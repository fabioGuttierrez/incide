from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Plan(models.Model):
    SLUGS = [
        ('gratuito', 'Gratuito'),
        ('starter', 'Starter'),
        ('profissional', 'Profissional'),
        ('premium', 'Premium'),
    ]
    name = models.CharField('Nome', max_length=100)
    slug = models.CharField('Identificador', max_length=50, choices=SLUGS, unique=True)
    monthly_query_limit = models.IntegerField(
        'Limite Mensal de Consultas',
        null=True,
        blank=True,
        help_text='Deixe em branco para ilimitado'
    )
    has_legal_basis = models.BooleanField('Ver Base Legal', default=False)
    has_favorites = models.BooleanField('Favoritos', default=False)
    has_history = models.BooleanField('Histórico', default=False)
    has_api_access = models.BooleanField('Acesso à API', default=False)
    price_brl = models.DecimalField('Preço (R$)', max_digits=8, decimal_places=2)
    is_active = models.BooleanField('Ativo', default=True)

    class Meta:
        verbose_name = 'Plano'
        verbose_name_plural = 'Planos'
        ordering = ['price_brl']

    def __str__(self):
        return self.name


class Subscription(models.Model):
    STATUS_CHOICES = [
        ('active', 'Ativo'),
        ('pending', 'Aguardando pagamento'),
        ('canceled', 'Cancelado'),
        ('past_due', 'Inadimplente'),
        ('trial', 'Trial'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='subscription',
        verbose_name='Usuário'
    )
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT, verbose_name='Plano')
    CYCLE_CHOICES = [
        ('monthly', 'Mensal'),
        ('annual', 'Anual'),
    ]

    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='trial')
    billing_cycle = models.CharField('Ciclo de Cobrança', max_length=10, choices=CYCLE_CHOICES, default='monthly')
    starts_at = models.DateTimeField('Início', default=timezone.now)
    ends_at = models.DateTimeField('Término', null=True, blank=True)
    asaas_customer_id = models.CharField('ID Cliente Asaas', max_length=100, blank=True, null=True)
    asaas_subscription_id = models.CharField('ID Assinatura Asaas', max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Assinatura'
        verbose_name_plural = 'Assinaturas'

    def __str__(self):
        return f'{self.user.username} — {self.plan}'

    @property
    def is_active(self):
        if self.status != 'active':
            return False
        if self.ends_at and self.ends_at < timezone.now():
            return False
        return True

    def queries_used_this_month(self):
        from apps.workspace.models import QueryLog
        return QueryLog.objects.filter(
            user=self.user,
            rubric__isnull=False,
            created_at__month=timezone.now().month,
            created_at__year=timezone.now().year,
        ).count()

    def queries_remaining(self):
        if self.plan.monthly_query_limit is None:
            return None
        used = self.queries_used_this_month()
        return max(0, self.plan.monthly_query_limit - used)


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Usuário',
    )
    phone = models.CharField('Telefone', max_length=20, blank=True)

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'

    def __str__(self):
        return f'Perfil de {self.user.username}'
