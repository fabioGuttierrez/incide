from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

app_name = 'v1'

urlpatterns = [
    # Auth
    path('auth/token/', TokenObtainPairView.as_view(), name='token-obtain'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    # Busca
    path('search/', views.search_view, name='search'),

    # Detalhe da rubrica (engine)
    path('rubrics/<int:pk>/', views.rubric_detail_view, name='rubric-detail'),

    # Favoritos
    path('favorites/', views.FavoriteListCreateView.as_view(), name='favorites-list'),
    path('favorites/<int:pk>/', views.FavoriteDestroyView.as_view(), name='favorites-delete'),

    # Histórico
    path('history/', views.HistoryListView.as_view(), name='history'),
]
