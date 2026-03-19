from django.contrib import admin
from .models import LegalNorm, LegalBasis


@admin.register(LegalNorm)
class LegalNormAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'norm_type', 'number', 'year', 'is_active']
    list_filter = ['norm_type', 'is_active', 'year']
    search_fields = ['number', 'title']
    list_editable = ['is_active']
    ordering = ['-year', 'norm_type']


@admin.register(LegalBasis)
class LegalBasisAdmin(admin.ModelAdmin):
    list_display = ['rubric', 'norm', 'article', 'is_primary']
    list_filter = ['is_primary', 'norm__norm_type']
    search_fields = ['rubric__name', 'norm__number', 'article']
    autocomplete_fields = ['rubric', 'norm']
