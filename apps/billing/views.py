import json
import logging

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from apps.accounts.models import Plan, Subscription
from apps.accounts.plan_check import get_user_plan
from .asaas import AsaasClient, AsaasError
from .forms import CheckoutForm

logger = logging.getLogger(__name__)


@login_required
def checkout_view(request, plan_slug):
    plan = get_object_or_404(Plan, slug=plan_slug, is_active=True)

    # Gratuito não tem checkout
    if plan.price_brl == 0:
        return redirect('catalog:home')

    # Evitar cobrança dupla: se já tem assinatura ativa para este plano
    try:
        sub = request.user.subscription
        if sub.asaas_subscription_id and sub.plan == plan and sub.is_active:
            return redirect('billing:success')
    except Subscription.DoesNotExist:
        pass

    annual_price = plan.price_brl * 10

    def _render_form(form):
        return render(request, 'billing/checkout.html', {
            'form': form,
            'plan': plan,
            'annual_price': annual_price,
        })

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            cpf_cnpj = form.cleaned_data['cpf_cnpj']
            billing_cycle = form.cleaned_data['billing_cycle']
            payment_method = 'pix'

            value = plan.price_brl if billing_cycle == 'monthly' else annual_price

            try:
                client = AsaasClient()
                customer_id = client.create_or_get_customer(
                    name=request.user.get_full_name() or request.user.username,
                    email=request.user.email,
                    cpf_cnpj=cpf_cnpj,
                )
                subscription = client.create_subscription(
                    customer_id=customer_id,
                    billing_type=payment_method,
                    billing_cycle=billing_cycle,
                    value=float(value),
                    description=f'Incide — {plan.name}',
                )
            except AsaasError as exc:
                logger.error('Asaas error on checkout for user %s: %s', request.user, exc)
                msg = str(exc) if settings.DEBUG else 'Erro ao processar pagamento. Tente novamente em instantes.'
                form.add_error(None, msg)
                return _render_form(form)

            # Atualiza (ou cria) Subscription local com status trial até webhook confirmar.
            Subscription.objects.update_or_create(
                user=request.user,
                defaults={
                    'plan': plan,
                    'status': 'trial',
                    'billing_cycle': billing_cycle,
                    'asaas_customer_id': customer_id,
                    'asaas_subscription_id': subscription['id'],
                },
            )

            invoice_url = (
                subscription.get('invoiceUrl')
                or subscription.get('bankSlipUrl')
                or client.get_subscription_invoice_url(subscription['id'])
            )
            if invoice_url:
                return redirect(invoice_url)

            # Fallback (sandbox sem URL disponível)
            return redirect('billing:success')
        return _render_form(form)

    return _render_form(CheckoutForm())


@login_required
def checkout_success_view(request):
    return render(request, 'billing/checkout_success.html')


# ---------------------------------------------------------------------------
# Webhook Asaas
# ---------------------------------------------------------------------------

@csrf_exempt
@require_POST
def asaas_webhook_view(request):
    # Verificar token de segurança
    token = request.headers.get('asaas-access-token', '')
    expected = getattr(settings, 'ASAAS_WEBHOOK_TOKEN', '')
    if expected and token != expected:
        logger.warning('Asaas webhook: token inválido recebido.')
        return HttpResponse(status=403)

    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponse(status=400)

    event = payload.get('event', '')
    payment = payload.get('payment', {})
    asaas_sub_id = payment.get('subscription')

    if not asaas_sub_id:
        # Cobrança avulsa sem assinatura — ignorar
        return HttpResponse(status=200)

    try:
        sub = Subscription.objects.get(asaas_subscription_id=asaas_sub_id)
    except Subscription.DoesNotExist:
        logger.warning('Webhook Asaas: assinatura %s não encontrada.', asaas_sub_id)
        return HttpResponse(status=200)

    if event in ('PAYMENT_CONFIRMED', 'PAYMENT_RECEIVED'):
        sub.status = 'active'
        sub.ends_at = None
        sub.save(update_fields=['status', 'ends_at', 'updated_at'])
        logger.info('Subscription %s ativada via webhook.', asaas_sub_id)

    elif event == 'PAYMENT_OVERDUE':
        sub.status = 'past_due'
        sub.save(update_fields=['status', 'updated_at'])

    elif event in ('SUBSCRIPTION_INACTIVATED', 'PAYMENT_DELETED', 'PAYMENT_REFUNDED'):
        sub.status = 'canceled'
        sub.save(update_fields=['status', 'updated_at'])

    return HttpResponse(status=200)
