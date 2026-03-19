"""
Cria os planos padrão do produto e atribui plano Starter ao admin.
Execute com: python manage.py seed_plans
"""
from django.core.management.base import BaseCommand
from django.db import transaction


PLANS = [
    {
        'name': 'Gratuito',
        'slug': 'gratuito',
        'monthly_query_limit': 10,
        'has_legal_basis': False,
        'has_favorites': False,
        'has_history': False,
        'has_api_access': False,
        'price_brl': '0.00',
    },
    {
        'name': 'Starter',
        'slug': 'starter',
        'monthly_query_limit': 100,
        'has_legal_basis': True,
        'has_favorites': True,
        'has_history': False,
        'has_api_access': False,
        'price_brl': '29.00',
    },
    {
        'name': 'Profissional',
        'slug': 'profissional',
        'monthly_query_limit': None,
        'has_legal_basis': True,
        'has_favorites': True,
        'has_history': True,
        'has_api_access': False,
        'price_brl': '59.00',
    },
    {
        'name': 'Premium',
        'slug': 'premium',
        'monthly_query_limit': None,
        'has_legal_basis': True,
        'has_favorites': True,
        'has_history': True,
        'has_api_access': True,
        'price_brl': '99.00',
    },
]


class Command(BaseCommand):
    help = 'Cria os planos padrão e atribui plano Starter ao admin'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        from apps.accounts.models import Plan, Subscription
        from django.contrib.auth.models import User

        self.stdout.write('Criando planos...')
        for p in PLANS:
            plan, created = Plan.objects.update_or_create(
                slug=p['slug'],
                defaults=p
            )
            status = 'criado' if created else 'atualizado'
            self.stdout.write(f'  {plan.name} (R${plan.price_brl}) — {status}')

        # Atribui plano Profissional ao admin (para desenvolvimento)
        try:
            admin = User.objects.get(username='admin')
            prof_plan = Plan.objects.get(slug='profissional')
            sub, created = Subscription.objects.update_or_create(
                user=admin,
                defaults={'plan': prof_plan, 'status': 'active'}
            )
            self.stdout.write(f'\nAdmin: plano {prof_plan.name} atribuido.')
        except User.DoesNotExist:
            pass

        self.stdout.write(self.style.SUCCESS(
            f'\n{Plan.objects.count()} planos configurados.'
        ))
