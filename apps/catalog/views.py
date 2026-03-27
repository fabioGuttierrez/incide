from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
import json

from apps.engine.analyzer import analyze_rubric, search_rubrics
from apps.engine.models import ContextualRule
from apps.workspace.models import Favorite, QueryLog, CompanyProfile
from apps.accounts.plan_check import check_query_limit, get_user_plan, require_plan
from .models import Rubric

_CONTEXT_KEY_LABELS = {
    'regime_tributario': 'Regime Tributário',
    'tipo_empresa': 'Tipo de Empresa',
    'tipo_empregado': 'Tipo de Empregado',
    'categoria_empregador': 'Categoria do Empregador',
}


def home(request):
    """Landing page para visitantes. Redireciona autenticados para o app."""
    if request.user.is_authenticated:
        return redirect('catalog:app_home')

    from apps.accounts.models import Plan
    total_rubricas = Rubric.objects.filter(is_published=True).count()
    plans = Plan.objects.filter(is_active=True).order_by('price_brl')

    return render(request, 'landing.html', {
        'total_rubricas': total_rubricas,
        'plans': plans,
    })


def app_home(request):
    """Tela principal do produto (busca). Só para autenticados."""
    total_rubricas = Rubric.objects.filter(is_published=True).count()
    return render(request, 'catalog/home.html', {'total_rubricas': total_rubricas})


def search_results(request):
    """Endpoint HTMX — retorna partial com resultados da busca."""
    query = request.GET.get('q', '').strip()
    rubrics = []

    if query:
        rubrics = search_rubrics(query)
        if request.user.is_authenticated:
            QueryLog.objects.create(
                user=request.user,
                search_term=query,
                session_key=request.session.session_key or '',
            )

    return render(request, 'catalog/partials/search_results.html', {
        'rubrics': rubrics,
        'query': query,
    })


def rubric_detail(request, slug):
    """Tela de detalhe de uma rubrica com análise completa do engine."""
    rubric = get_object_or_404(
        Rubric.objects.prefetch_related(
            'related_rubrics__incidence',
            'related_rubrics__category',
        ),
        slug=slug,
        is_published=True,
    )

    can_query, remaining = check_query_limit(request.user)
    if not can_query:
        from apps.accounts.models import Plan
        plan = get_user_plan(request.user)
        upgrade_plans = Plan.objects.filter(
            is_active=True, price_brl__gt=plan.price_brl if plan else 0
        ).order_by('price_brl')
        return render(request, 'accounts/query_limit_reached.html', {
            'plan': plan,
            'rubric': rubric,
            'upgrade_plans': upgrade_plans,
        }, status=403)

    try:
        result = analyze_rubric(rubric_id=rubric.id)
    except Exception:
        return render(request, 'catalog/rubric_detail_error.html', {'rubric': rubric})

    plan = get_user_plan(request.user)
    show_legal_basis = bool(plan and plan.has_legal_basis and request.user.is_authenticated)

    from apps.accounts.models import Plan as PlanModel
    upgrade_plan = PlanModel.objects.filter(
        is_active=True,
        price_brl__gt=plan.price_brl if plan else 0,
    ).order_by('price_brl').first()

    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, rubric=rubric).exists()
        QueryLog.objects.create(
            user=request.user,
            rubric=rubric,
            session_key=request.session.session_key or '',
        )

    context_options = _build_context_options(rubric)
    company_profiles = []
    if request.user.is_authenticated:
        company_profiles = [
            {'name': p.name, 'context_json': json.dumps(p.context)}
            for p in CompanyProfile.objects.filter(user=request.user)
        ]

    # SEO: meta description dinâmica por rubrica
    if rubric.description:
        desc_snippet = rubric.description[:110].rstrip(' .,;')
        meta_description = f"{rubric.name}: saiba se incide INSS, FGTS e IRRF. {desc_snippet}. Análise trabalhista com base legal para contadores e analistas de DP."
    else:
        meta_description = f"Saiba se {rubric.name} incide INSS, FGTS e IRRF. Análise completa com fundamento em lei (CLT, eSocial) para contadores e analistas de Departamento Pessoal."

    return render(request, 'catalog/rubric_detail.html', {
        'result': result,
        'rubric': rubric,
        'is_favorite': is_favorite,
        'show_legal_basis': show_legal_basis,
        'queries_remaining': remaining,
        'plan': plan,
        'upgrade_plan': upgrade_plan,
        'context_options': context_options,
        'company_profiles': company_profiles,
        'meta_description': meta_description,
    })


def _build_context_options(rubric):
    """
    Retorna dict {condition_key: {label, options: [{value, label}]}}
    para cada chave de regra contextual desta rubrica.
    """
    rules = ContextualRule.objects.filter(rubric=rubric).values(
        'condition_key', 'condition_value'
    )
    result = {}
    for rule in rules:
        key = rule['condition_key']
        if key not in result:
            result[key] = {
                'label': _CONTEXT_KEY_LABELS.get(key, key.replace('_', ' ').title()),
                'options': [],
            }
        value = rule['condition_value']
        result[key]['options'].append({
            'value': value,
            'label': value.replace('_', ' ').title(),
        })
    return result


@require_POST
@login_required
def rubric_context_analysis(request, rubric_id):
    """Endpoint HTMX — reanálise da rubrica com contexto do usuário."""
    plan = get_user_plan(request.user)
    if not (plan and plan.has_legal_basis):
        from django.http import HttpResponse
        return HttpResponse(status=403)

    rubric = get_object_or_404(Rubric, id=rubric_id, is_published=True)

    context = {
        k: v for k, v in request.POST.items()
        if k != 'csrfmiddlewaretoken' and v
    }

    try:
        result = analyze_rubric(rubric_id=rubric.id, context=context or None)
    except Exception:
        from django.http import HttpResponse
        return HttpResponse("Erro ao processar contexto.", status=500)

    return render(request, 'catalog/partials/incidence_analysis.html', {
        'result': result,
    })


@require_POST
@login_required
def toggle_favorite(request, rubric_id):
    plan = get_user_plan(request.user)
    if not (plan and plan.has_favorites):
        from django.http import HttpResponse
        return HttpResponse(status=403)
    rubric = get_object_or_404(Rubric, id=rubric_id, is_published=True)
    favorite = Favorite.objects.filter(user=request.user, rubric=rubric).first()

    if favorite:
        favorite.delete()
        is_favorite = False
    else:
        Favorite.objects.create(user=request.user, rubric=rubric)
        is_favorite = True

    return render(request, 'catalog/partials/favorite_button.html', {
        'is_favorite': is_favorite,
        'rubric': rubric,
    })


@login_required
@require_plan('has_favorites')
def favorites_list(request):
    favorites = Favorite.objects.filter(user=request.user).select_related(
        'rubric', 'rubric__category', 'rubric__esocial_nature', 'rubric__incidence'
    )
    return render(request, 'catalog/favorites.html', {'favorites': favorites})


@login_required
@require_plan('has_history')
def history_list(request):
    logs = QueryLog.objects.filter(user=request.user).select_related('rubric').order_by('-created_at')[:50]
    return render(request, 'catalog/history.html', {'logs': logs})


@login_required
def profiles_list(request):
    """Gerenciamento de perfis de empresa salvos."""
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if name:
            context = {
                k: v for k, v in request.POST.items()
                if k not in ('csrfmiddlewaretoken', 'name') and v
            }
            CompanyProfile.objects.create(user=request.user, name=name, context=context)
        return redirect('catalog:profiles')

    profiles = CompanyProfile.objects.filter(user=request.user)
    # Todos os pares (chave, valor) únicos de regras contextuais no sistema
    all_context_options = _build_global_context_options()
    return render(request, 'catalog/profiles.html', {
        'profiles': profiles,
        'all_context_options': all_context_options,
    })


@require_POST
@login_required
def profile_delete(request, profile_id):
    profile = get_object_or_404(CompanyProfile, id=profile_id, user=request.user)
    profile.delete()
    return redirect('catalog:profiles')


def _build_global_context_options():
    """Retorna todos os pares de contexto disponíveis no sistema."""
    rules = ContextualRule.objects.values('condition_key', 'condition_value').distinct()
    result = {}
    for rule in rules:
        key = rule['condition_key']
        if key not in result:
            result[key] = {
                'label': _CONTEXT_KEY_LABELS.get(key, key.replace('_', ' ').title()),
                'options': [],
            }
        value = rule['condition_value']
        result[key]['options'].append({
            'value': value,
            'label': value.replace('_', ' ').title(),
        })
    return result
