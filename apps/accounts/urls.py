from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('entrar/', views.login_view, name='login'),
    path('registrar/', views.register_view, name='register'),
    path('sair/', views.logout_view, name='logout'),
]
