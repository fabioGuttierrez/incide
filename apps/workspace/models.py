from django.db import models
from django.contrib.auth.models import User


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Usuário'
    )
    rubric = models.ForeignKey(
        'catalog.Rubric',
        on_delete=models.CASCADE,
        related_name='favorited_by',
        verbose_name='Rubrica'
    )
    note = models.TextField(
        'Anotação',
        blank=True,
        help_text='Anotação pessoal sobre esta rubrica'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Favorito'
        verbose_name_plural = 'Favoritos'
        unique_together = ['user', 'rubric']
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} → {self.rubric}'


class QueryLog(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='query_logs',
        verbose_name='Usuário'
    )
    rubric = models.ForeignKey(
        'catalog.Rubric',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='query_logs',
        verbose_name='Rubrica'
    )
    search_term = models.CharField('Termo de Busca', max_length=255, blank=True)
    session_key = models.CharField('Sessão', max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Consulta'
        verbose_name_plural = 'Consultas'
        ordering = ['-created_at']

    def __str__(self):
        who = self.user.username if self.user else 'anônimo'
        return f'{who} → {self.rubric or self.search_term}'
