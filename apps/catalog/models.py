from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    TYPES = [
        ('provento', 'Provento'),
        ('desconto', 'Desconto'),
        ('informativo', 'Informativo'),
        ('base', 'Base de Cálculo'),
    ]
    name = models.CharField('Nome', max_length=100)
    slug = models.SlugField(unique=True)
    category_type = models.CharField('Tipo', max_length=20, choices=TYPES)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class EsocialNature(models.Model):
    code = models.CharField('Código', max_length=10, unique=True)
    description = models.CharField('Descrição', max_length=255)
    is_salary_nature = models.BooleanField(
        'Natureza Salarial',
        help_text='Define se possui natureza salarial para fins previdenciários'
    )

    class Meta:
        verbose_name = 'Natureza eSocial'
        verbose_name_plural = 'Naturezas eSocial'
        ordering = ['code']

    def __str__(self):
        return f'{self.code} - {self.description}'


class Rubric(models.Model):
    name = models.CharField('Nome', max_length=255)
    slug = models.SlugField(unique=True, max_length=300)
    code = models.CharField('Código', max_length=50, blank=True)
    description = models.TextField('Descrição')
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        verbose_name='Categoria'
    )
    esocial_nature = models.ForeignKey(
        EsocialNature,
        on_delete=models.PROTECT,
        verbose_name='Natureza eSocial'
    )

    is_published = models.BooleanField('Publicada', default=False)
    last_legal_review = models.DateField('Última Revisão Legal', null=True, blank=True)
    reviewed_by = models.CharField('Revisado por', max_length=255, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Rubrica'
        verbose_name_plural = 'Rubricas'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
