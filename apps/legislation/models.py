from django.db import models


class LegalNorm(models.Model):
    TYPES = [
        ('lei', 'Lei'),
        ('decreto', 'Decreto'),
        ('in_rfb', 'Instrução Normativa RFB'),
        ('resolucao', 'Resolução'),
        ('clt', 'CLT'),
        ('portaria', 'Portaria'),
        ('jurisprudencia', 'Jurisprudência'),
        ('outros', 'Outros'),
    ]
    norm_type = models.CharField('Tipo', max_length=20, choices=TYPES)
    number = models.CharField('Número', max_length=50)
    year = models.IntegerField('Ano')
    title = models.CharField('Título', max_length=500)
    official_link = models.URLField('Link Oficial', blank=True)
    is_active = models.BooleanField(
        'Vigente',
        default=True,
        help_text='Desmarque se a norma foi revogada'
    )

    class Meta:
        verbose_name = 'Norma Legal'
        verbose_name_plural = 'Normas Legais'
        ordering = ['-year', 'norm_type', 'number']

    def __str__(self):
        return f'{self.get_norm_type_display()} {self.number}/{self.year}'


class LegalBasis(models.Model):
    rubric = models.ForeignKey(
        'catalog.Rubric',
        on_delete=models.CASCADE,
        related_name='legal_basis',
        verbose_name='Rubrica'
    )
    norm = models.ForeignKey(
        LegalNorm,
        on_delete=models.PROTECT,
        verbose_name='Norma'
    )
    article = models.CharField('Artigo', max_length=100, blank=True)
    excerpt = models.TextField('Excerto da Lei', blank=True)
    is_primary = models.BooleanField(
        'Base Principal',
        default=False,
        help_text='A fundamentação primária desta rubrica'
    )

    class Meta:
        verbose_name = 'Base Legal'
        verbose_name_plural = 'Bases Legais'
        ordering = ['-is_primary', 'norm__year']

    def __str__(self):
        article_str = f' - {self.article}' if self.article else ''
        return f'{self.norm}{article_str}'
