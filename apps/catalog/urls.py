from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.home, name='home'),
    path('app/', views.app_home, name='app_home'),
    path('busca/resultados/', views.search_results, name='search_results'),
    path('rubrica/<slug:slug>/', views.rubric_detail, name='rubric_detail'),
    path('rubrica/<int:rubric_id>/favorito/', views.toggle_favorite, name='toggle_favorite'),
    path('rubrica/<int:rubric_id>/contexto/', views.rubric_context_analysis, name='rubric_context'),
    path('favoritos/', views.favorites_list, name='favorites'),
    path('historico/', views.history_list, name='history'),
    path('perfis/', views.profiles_list, name='profiles'),
    path('perfis/<int:profile_id>/deletar/', views.profile_delete, name='profile_delete'),
]
