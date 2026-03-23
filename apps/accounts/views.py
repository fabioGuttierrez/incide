import calendar

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from apps.accounts.forms import RegisterForm, ProfileEditForm
from apps.accounts.models import Plan, Subscription, UserProfile


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
    user = request.user
    profile, _ = UserProfile.objects.get_or_create(user=user)

    try:
        subscription = user.subscription
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
            month = starts.month + 1
            year = starts.year
            if month > 12:
                month = 1
                year += 1
            day = min(starts.day, calendar.monthrange(year, month)[1])
            period_end = starts.replace(year=year, month=month, day=day)

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, current_user=user)
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            if form.cleaned_data['email']:
                user.email = form.cleaned_data['email']
            user.save(update_fields=['first_name', 'last_name', 'email'])
            profile.phone = form.cleaned_data['phone']
            profile.save(update_fields=['phone'])
            messages.success(request, 'Dados atualizados com sucesso.')
            return redirect('accounts:profile')
    else:
        form = ProfileEditForm(initial={
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'phone': profile.phone,
        }, current_user=user)

    upgrade_plans = Plan.objects.filter(
        is_active=True, price_brl__gt=0
    ).order_by('price_brl')

    return render(request, 'accounts/profile.html', {
        'subscription': subscription,
        'upgrade_plans': upgrade_plans,
        'period_end': period_end,
        'form': form,
        'profile': profile,
    })
