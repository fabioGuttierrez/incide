from django.contrib import admin
from .models import Favorite, QueryLog


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'rubric', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'rubric__name']
    readonly_fields = ['created_at']


@admin.register(QueryLog)
class QueryLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'rubric', 'search_term', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'rubric__name', 'search_term']
    readonly_fields = ['created_at']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
