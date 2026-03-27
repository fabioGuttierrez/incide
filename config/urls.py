from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView

from apps.catalog.sitemaps import RubricSitemap, StaticSitemap

sitemaps = {
    'rubricas': RubricSitemap,
    'static': StaticSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.api.urls')),
    path('conta/', include('apps.accounts.urls', namespace='accounts')),
    path('billing/', include('apps.billing.urls', namespace='billing')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps, 'domain': 'incide.bildee.com.br'}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    path('', include('apps.catalog.urls', namespace='catalog')),
]
