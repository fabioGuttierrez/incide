from django.contrib import admin
from .models import Category, EsocialNature, Rubric


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category_type', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['category_type']


@admin.register(EsocialNature)
class EsocialNatureAdmin(admin.ModelAdmin):
    list_display = ['code', 'description', 'is_salary_nature']
    list_filter = ['is_salary_nature']
    search_fields = ['code', 'description']


class LegalBasisInline(admin.TabularInline):
    from apps.legislation.models import LegalBasis
    model = LegalBasis
    extra = 1
    fields = ['norm', 'article', 'excerpt', 'is_primary']
    autocomplete_fields = ['norm']


class IncidenceInline(admin.StackedInline):
    from apps.engine.models import Incidence
    model = Incidence
    extra = 0
    max_num = 1
    fields = [
        ('inss', 'fgts', 'irrf'),
        'inss_observation', 'fgts_observation', 'irrf_observation',
        'risk_level',
        ('recently_changed', 'change_date'),
        'change_note',
    ]


@admin.register(Rubric)
class RubricAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'code', 'category', 'esocial_nature',
        'is_published', 'last_legal_review'
    ]
    list_filter = ['is_published', 'category', 'esocial_nature__is_salary_nature']
    search_fields = ['name', 'code', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_published']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [IncidenceInline, LegalBasisInline]

    fieldsets = (
        ('Identificação', {
            'fields': ('name', 'slug', 'code', 'description')
        }),
        ('Classificação', {
            'fields': ('category', 'esocial_nature')
        }),
        ('Publicação e Revisão', {
            'fields': ('is_published', 'last_legal_review', 'reviewed_by')
        }),
        ('Auditoria', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category', 'esocial_nature')
