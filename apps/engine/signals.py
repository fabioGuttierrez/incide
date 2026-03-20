"""
Signals do engine — dispara notificações por e-mail quando
uma rubrica é marcada como recentemente alterada.
"""
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver


@receiver(pre_save, sender='engine.Incidence')
def _capture_old_recently_changed(sender, instance, **kwargs):
    """Salva o valor anterior de recently_changed antes de sobrescrever."""
    if instance.pk:
        try:
            old = sender.objects.get(pk=instance.pk)
            instance._old_recently_changed = old.recently_changed
        except sender.DoesNotExist:
            instance._old_recently_changed = False
    else:
        instance._old_recently_changed = False


@receiver(post_save, sender='engine.Incidence')
def _notify_rubric_changed(sender, instance, created, **kwargs):
    """
    Envia e-mail para todos os usuários que consultaram esta rubrica
    quando recently_changed passa de False → True.
    """
    old = getattr(instance, '_old_recently_changed', False)
    if created or not instance.recently_changed or old:
        return  # só dispara na transição False → True

    _send_change_notifications(instance)


def _send_change_notifications(incidence):
    from apps.workspace.models import QueryLog
    from django.core.mail import EmailMultiAlternatives
    from django.template.loader import render_to_string
    from django.conf import settings

    recipients = (
        QueryLog.objects
        .filter(rubric=incidence.rubric, user__isnull=False, user__email__gt='')
        .values_list('user__email', 'user__first_name')
        .distinct()
    )

    if not recipients:
        return

    rubric = incidence.rubric
    subject = f'[Incide] Atualização legislativa: {rubric.name}'

    for email, first_name in recipients:
        context = {
            'rubric': rubric,
            'change_note': incidence.change_note,
            'change_date': incidence.change_date,
            'first_name': first_name or 'Olá',
        }
        text_body = render_to_string('emails/rubric_changed.txt', context)
        html_body = render_to_string('emails/rubric_changed.html', context)

        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_body,
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@incide.com.br'),
            to=[email],
        )
        msg.attach_alternative(html_body, 'text/html')
        msg.send(fail_silently=True)
