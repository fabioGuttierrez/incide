from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from apps.engine.analyzer import analyze_rubric, search_rubrics
from apps.workspace.models import Favorite, QueryLog
from apps.accounts.plan_check import check_query_limit, get_user_plan
from .models import Rubric


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
    rubric = get_object_or_404(Rubric, slug=slug, is_published=True)

    can_query, remaining = check_query_limit(request.user)
    if not can_query:
        plan = get_user_plan(request.user)
        return render(request, 'accounts/query_limit_reached.html', {
            'plan': plan,
            'rubric': rubric,
        }, status=403)

    try:
        result = analyze_rubric(rubric_id=rubric.id)
    except Exception:
        return render(request, 'catalog/rubric_detail_error.html', {'rubric': rubric})

    plan = get_user_plan(request.user)
    show_legal_basis = bool(plan and plan.has_legal_basis and request.user.is_authenticated)

    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, rubric=rubric).exists()
        QueryLog.objects.create(
            user=request.user,
            rubric=rubric,
            session_key=request.session.session_key or '',
        )

    return render(request, 'catalog/rubric_detail.html', {
        'result': result,
        'rubric': rubric,
        'is_favorite': is_favorite,
        'show_legal_basis': show_legal_basis,
        'queries_remaining': remaining,
        'plan': plan,
    })


@require_POST
@login_required
def toggle_favorite(request, rubric_id):
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
def favorites_list(request):
    favorites = Favorite.objects.filter(user=request.user).select_related(
        'rubric', 'rubric__category', 'rubric__esocial_nature', 'rubric__incidence'
    )
    return render(request, 'catalog/favorites.html', {'favorites': favorites})


@login_required
def history_list(request):
    logs = QueryLog.objects.filter(user=request.user).select_related('rubric').order_by('-created_at')[:50]
    return render(request, 'catalog/history.html', {'logs': logs})
