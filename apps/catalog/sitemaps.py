from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Rubric


class RubricSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8
    protocol = 'https'

    def items(self):
        return Rubric.objects.filter(is_published=True).order_by('-updated_at')

    def location(self, obj):
        return reverse('catalog:rubric_detail', args=[obj.slug])

    def lastmod(self, obj):
        return obj.updated_at


class StaticSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 1.0
    protocol = 'https'

    def items(self):
        return ['landing']

    def location(self, item):
        return reverse('catalog:home')
