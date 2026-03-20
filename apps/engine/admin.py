from django.contrib import admin
from .models import Incidence, ContextualRule


@admin.register(Incidence)
class IncidenceAdmin(admin.ModelAdmin):
    list_display = [
        'rubric', 'inss', 'fgts', 'irrf', 'iss',
        'risk_level', 'recently_changed', 'updated_at'
    ]
    list_filter = ['inss', 'fgts', 'irrf', 'iss', 'risk_level', 'recently_changed']
    search_fields = ['rubric__name']
    list_editable = ['recently_changed']
    readonly_fields = ['updated_at']

    fieldsets = (
        ('Rubrica', {'fields': ('rubric',)}),
        ('Incidências', {
            'fields': (
                ('inss', 'fgts', 'irrf', 'iss'),
                'inss_observation',
                'fgts_observation',
                'irrf_observation',
                'iss_observation',
            )
        }),
        ('Risco e Alertas', {
            'fields': (
                'risk_level',
                'risk_reason',
                ('recently_changed', 'change_date'),
                'change_note',
            )
        }),
        ('Auditoria', {'fields': ('updated_at',), 'classes': ('collapse',)}),
    )


@admin.register(ContextualRule)
class ContextualRuleAdmin(admin.ModelAdmin):
    list_display = ['rubric', 'condition_description', 'condition_key', 'condition_value']
    list_filter = ['condition_key']
    search_fields = ['rubric__name', 'condition_description']
    fieldsets = (
        ('Vínculo', {'fields': ('rubric',)}),
        ('Condição', {
            'fields': ('condition_key', 'condition_value', 'condition_description'),
            'description': (
                'condition_key: chave do contexto (ex: regime_tributario). '
                'condition_value: valor esperado (ex: simples). '
                'condition_description: texto curto exibido ao usuário quando a regra é aplicada.'
            ),
        }),
        ('Substituição de incidência', {
            'fields': ('override_inss', 'override_fgts', 'override_irrf', 'explanation'),
            'description': 'Deixe em branco os campos que não devem ser alterados pelo contexto.',
        }),
    )
