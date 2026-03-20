from django.urls import path
from . import views

app_name = 'billing'

urlpatterns = [
    path('checkout/<slug:plan_slug>/', views.checkout_view, name='checkout'),
    path('sucesso/', views.checkout_success_view, name='success'),
    path('webhook/asaas/', views.asaas_webhook_view, name='webhook_asaas'),
]
