from django.contrib import admin
from .models import Plan, Subscription


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'slug', 'price_brl',
        'monthly_query_limit', 'has_legal_basis',
        'has_favorites', 'has_api_access', 'is_active'
    ]
    list_editable = ['is_active']


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'plan', 'status', 'starts_at', 'ends_at', 'is_active']
    list_filter = ['status', 'plan']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']
