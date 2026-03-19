from rest_framework import serializers
from apps.catalog.models import Rubric, Category, EsocialNature
from apps.workspace.models import Favorite, QueryLog


class EsocialNatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = EsocialNature
        fields = ['code', 'description', 'is_salary_nature']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'slug', 'category_type']


class RubricListSerializer(serializers.ModelSerializer):
    """Usado na listagem e busca — dados essenciais."""
    category = serializers.StringRelatedField()
    esocial_nature = EsocialNatureSerializer()

    # Incidências resumidas direto na listagem
    inss = serializers.SerializerMethodField()
    fgts = serializers.SerializerMethodField()
    irrf = serializers.SerializerMethodField()

    class Meta:
        model = Rubric
        fields = [
            'id', 'name', 'slug', 'code',
            'category', 'esocial_nature',
            'inss', 'fgts', 'irrf',
        ]

    def get_inss(self, obj):
        return getattr(getattr(obj, 'incidence', None), 'inss', None)

    def get_fgts(self, obj):
        return getattr(getattr(obj, 'incidence', None), 'fgts', None)

    def get_irrf(self, obj):
        return getattr(getattr(obj, 'incidence', None), 'irrf', None)


class LegalBasisSerializer(serializers.Serializer):
    norm = serializers.CharField()
    article = serializers.CharField()
    excerpt = serializers.CharField()
    is_primary = serializers.BooleanField()
    official_link = serializers.URLField()


class IncidenceResultSerializer(serializers.Serializer):
    """Serializa o resultado do analyzer — resposta completa da consulta."""
    rubric_id = serializers.IntegerField()
    rubric_name = serializers.CharField()
    rubric_slug = serializers.CharField()
    rubric_code = serializers.CharField()
    category = serializers.CharField()
    esocial_nature_code = serializers.CharField()
    esocial_nature_description = serializers.CharField()
    is_salary_nature = serializers.BooleanField()

    inss = serializers.BooleanField()
    fgts = serializers.BooleanField()
    irrf = serializers.BooleanField()

    inss_observation = serializers.CharField()
    fgts_observation = serializers.CharField()
    irrf_observation = serializers.CharField()

    risk_level = serializers.CharField()
    recently_changed = serializers.BooleanField()
    change_note = serializers.CharField()
    change_date = serializers.CharField(allow_null=True)

    explanation = serializers.CharField()
    legal_basis = LegalBasisSerializer(many=True)
    contextual_rules_applied = serializers.ListField(child=serializers.CharField())


class FavoriteSerializer(serializers.ModelSerializer):
    rubric_name = serializers.CharField(source='rubric.name', read_only=True)
    rubric_slug = serializers.CharField(source='rubric.slug', read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'rubric', 'rubric_name', 'rubric_slug', 'note', 'created_at']
        read_only_fields = ['id', 'created_at']


class QueryLogSerializer(serializers.ModelSerializer):
    rubric_name = serializers.CharField(source='rubric.name', read_only=True)

    class Meta:
        model = QueryLog
        fields = ['id', 'rubric', 'rubric_name', 'search_term', 'created_at']
        read_only_fields = ['id', 'created_at']
