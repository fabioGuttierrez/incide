"""
Utilitário para verificação de plano e limites de consulta.
"""
from functools import wraps
from django.shortcuts import render
from django.http import HttpResponse


def get_user_plan(user):
    """
    Retorna o plano ativo do usuário.
    Se não tiver assinatura, retorna o plano Gratuito.
    """
    from apps.accounts.models import Plan, Subscription

    if not user.is_authenticated:
        return Plan.objects.filter(slug='gratuito').first()

    try:
        sub = user.subscription
        if sub.is_active:
            return sub.plan
    except Exception:
        pass

    return Plan.objects.filter(slug='gratuito').first()


def check_query_limit(user):
    """
    Verifica se o usuário pode fazer mais consultas este mês.
    Retorna (pode_consultar: bool, restantes: int|None)
    """
    if not user.is_authenticated:
        # Anônimos: 3 consultas por sessão (controlado no frontend)
        return True, None

    plan = get_user_plan(user)
    if plan is None or plan.monthly_query_limit is None:
        return True, None  # ilimitado

    try:
        sub = user.subscription
        remaining = sub.queries_remaining()
        return remaining > 0, remaining
    except Exception:
        # Sem assinatura — aplica limite do plano gratuito
        from apps.workspace.models import QueryLog
        from django.utils import timezone
        used = QueryLog.objects.filter(
            user=user,
            rubric__isnull=False,
            created_at__month=timezone.now().month,
            created_at__year=timezone.now().year,
        ).count()
        remaining = max(0, plan.monthly_query_limit - used)
        return remaining > 0, remaining


def require_plan(feature: str):
    """
    Decorator que verifica se o plano do usuário tem acesso a um feature.
    Uso: @require_plan('has_legal_basis')
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapped(request, *args, **kwargs):
            from apps.accounts.models import Plan
            plan = get_user_plan(request.user)
            if plan and getattr(plan, feature, False):
                return view_func(request, *args, **kwargs)
            upgrade_plans = Plan.objects.filter(
                is_active=True, price_brl__gt=plan.price_brl if plan else 0
            ).order_by('price_brl')
            return render(request, 'accounts/plan_required.html', {
                'feature': feature,
                'plan': plan,
                'upgrade_plans': upgrade_plans,
            }, status=403)
        return wrapped
    return decorator


class HasApiAccess:
    """
    Permissão DRF: exige plano com has_api_access=True.
    Uso: permission_classes = [HasApiAccess]
    """
    def has_permission(self, request, view):
        plan = get_user_plan(request.user)
        return bool(plan and plan.has_api_access)

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
