from django.db import models


class Incidence(models.Model):
    RISK_LEVELS = [
        ('low', 'Baixo'),
        ('medium', 'Médio'),
        ('high', 'Alto'),
    ]

    rubric = models.OneToOneField(
        'catalog.Rubric',
        on_delete=models.CASCADE,
        related_name='incidence',
        verbose_name='Rubrica'
    )

    inss = models.BooleanField('Incide INSS')
    fgts = models.BooleanField('Incide FGTS')
    irrf = models.BooleanField('Incide IRRF')

    inss_observation = models.TextField('Observação INSS', blank=True)
    fgts_observation = models.TextField('Observação FGTS', blank=True)
    irrf_observation = models.TextField('Observação IRRF', blank=True)

    risk_level = models.CharField(
        'Nível de Risco',
        max_length=10,
        choices=RISK_LEVELS,
        default='low',
        help_text='Risco de autuação em caso de erro nesta rubrica'
    )

    recently_changed = models.BooleanField(
        'Alterado Recentemente',
        default=False,
        help_text='Sinaliza ao usuário que houve mudança legislativa recente'
    )
    change_note = models.TextField('Nota de Alteração', blank=True)
    change_date = models.DateField('Data da Alteração', null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Incidência'
        verbose_name_plural = 'Incidências'

    def __str__(self):
        flags = []
        if self.inss:
            flags.append('INSS')
        if self.fgts:
            flags.append('FGTS')
        if self.irrf:
            flags.append('IRRF')
        return f'{self.rubric} → {", ".join(flags) if flags else "Nenhuma incidência"}'


class ContextualRule(models.Model):
    """
    Regras que modificam a incidência padrão conforme o contexto da empresa.
    Ex: 'Quando optante pelo Simples Nacional, hora extra não incide INSS patronal'.
    """
    rubric = models.ForeignKey(
        'catalog.Rubric',
        on_delete=models.CASCADE,
        related_name='contextual_rules',
        verbose_name='Rubrica'
    )
    condition_description = models.CharField('Condição', max_length=500)
    condition_key = models.CharField(
        'Chave da Condição',
        max_length=100,
        help_text='Ex: regime_tributario, tipo_empresa'
    )
    condition_value = models.CharField(
        'Valor da Condição',
        max_length=100,
        help_text='Ex: simples, mei'
    )
    override_inss = models.BooleanField('Substitui INSS', null=True, blank=True)
    override_fgts = models.BooleanField('Substitui FGTS', null=True, blank=True)
    override_irrf = models.BooleanField('Substitui IRRF', null=True, blank=True)
    explanation = models.TextField('Explicação da Regra', blank=True)

    class Meta:
        verbose_name = 'Regra Contextual'
        verbose_name_plural = 'Regras Contextuais'

    def __str__(self):
        return f'{self.rubric} | {self.condition_description}'
