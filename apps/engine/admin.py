from django.contrib import admin
from .models import Incidence, ContextualRule


@admin.register(Incidence)
class IncidenceAdmin(admin.ModelAdmin):
    list_display = [
        'rubric', 'inss', 'fgts', 'irrf',
        'risk_level', 'recently_changed', 'updated_at'
    ]
    list_filter = ['inss', 'fgts', 'irrf', 'risk_level', 'recently_changed']
    search_fields = ['rubric__name']
    list_editable = ['recently_changed']
    readonly_fields = ['updated_at']

    fieldsets = (
        ('Rubrica', {'fields': ('rubric',)}),
        ('Incidências', {
            'fields': (
                ('inss', 'fgts', 'irrf'),
                'inss_observation',
                'fgts_observation',
                'irrf_observation',
            )
        }),
        ('Risco e Alertas', {
            'fields': (
                'risk_level',
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
