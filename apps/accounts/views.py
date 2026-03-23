import calendar

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from apps.accounts.forms import RegisterForm
from apps.accounts.models import Plan, Subscription


def login_view(request):
    if request.user.is_authenticated:
        return redirect('catalog:home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
        messages.error(request, 'Usuário ou senha inválidos.')
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('catalog:home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            gratuito = Plan.objects.filter(slug='gratuito', is_active=True).first()
            if gratuito:
                Subscription.objects.get_or_create(user=user, defaults={'plan': gratuito, 'status': 'active'})
            login(request, user)
            messages.success(request, 'Conta criada com sucesso! Bem-vindo ao Incide.')
            return redirect('catalog:home')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('catalog:home')


@login_required
def profile_view(request):
    try:
        subscription = request.user.subscription
    except Subscription.DoesNotExist:
        subscription = None

    period_end = None
    if subscription and subscription.starts_at:
        starts = subscription.starts_at
        if subscription.billing_cycle == 'annual':
            year = starts.year + 1
            month = starts.month
            day = min(starts.day, calendar.monthrange(year, month)[1])
            period_end = starts.replace(year=year, month=month, day=day)
        else:
            # monthly: advance 1 month
            month = starts.month + 1
            year = starts.year
            if month > 12:
                month = 1
                year += 1
            day = min(starts.day, calendar.monthrange(year, month)[1])
            period_end = starts.replace(year=year, month=month, day=day)

    upgrade_plans = Plan.objects.filter(
        is_active=True, price_brl__gt=0
    ).order_by('price_brl')

    return render(request, 'accounts/profile.html', {
        'subscription': subscription,
        'upgrade_plans': upgrade_plans,
        'period_end': period_end,
    })
