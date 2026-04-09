"""
Analisador principal de rubricas.

Recebe o ID de uma rubrica e, opcionalmente, um contexto
(ex: regime tributário da empresa), e retorna a decisão
completa de incidências com explicação fundamentada.
"""

from dataclasses import dataclass, field
from typing import Optional
from .explainer import generate_explanation


@dataclass
class LegalBasisResult:
    norm: str
    article: str
    excerpt: str
    is_primary: bool
    official_link: str


@dataclass
class IncidenceResult:
    rubric_id: int
    rubric_name: str
    rubric_slug: str
    rubric_code: str
    category: str
    esocial_nature_code: str
    esocial_nature_description: str
    is_salary_nature: bool

    inss: bool
    fgts: bool
    irrf: bool
    iss: bool

    inss_observation: str
    fgts_observation: str
    irrf_observation: str
    iss_observation: str

    risk_level: str
    risk_reason: str
    recently_changed: bool
    change_note: str
    change_date: Optional[str]

    explanation: str
    legal_basis: list[LegalBasisResult] = field(default_factory=list)
    contextual_rules_applied: list[str] = field(default_factory=list)


def analyze_rubric(rubric_id: int, context: Optional[dict] = None) -> IncidenceResult:
    """
    Analisa uma rubrica e retorna a decisão completa de incidências.

    Args:
        rubric_id: ID da rubrica a analisar
        context: dicionário opcional com contexto da empresa
                 Ex: {'regime_tributario': 'simples', 'tipo_empresa': 'mei'}

    Returns:
        IncidenceResult com todos os dados estruturados

    Raises:
        Rubric.DoesNotExist: se a rubrica não for encontrada ou não estiver publicada
        Incidence.DoesNotExist: se a incidência ainda não foi cadastrada
    """
    from apps.catalog.models import Rubric
    from apps.engine.models import Incidence, ContextualRule
    from apps.legislation.models import LegalBasis

    rubric = Rubric.objects.select_related(
        'category',
        'esocial_nature'
    ).get(id=rubric_id, is_published=True)

    incidence = Incidence.objects.get(rubric=rubric)

    legal_basis_qs = list(
        LegalBasis.objects.filter(rubric=rubric)
        .select_related('norm')
        .order_by('-is_primary')
    )

    rules_applied = []
    if context:
        incidence, rules_applied = _apply_contextual_rules(rubric, incidence, context)

    explanation = generate_explanation(rubric, incidence, legal_basis_qs)

    legal_basis_results = [
        LegalBasisResult(
            norm=str(lb.norm),
            article=lb.article,
            excerpt=lb.excerpt,
            is_primary=lb.is_primary,
            official_link=lb.norm.official_link,
        )
        for lb in legal_basis_qs
    ]

    return IncidenceResult(
        rubric_id=rubric.id,
        rubric_name=rubric.name,
        rubric_slug=rubric.slug,
        rubric_code=rubric.code,
        category=rubric.category.name,
        esocial_nature_code=rubric.esocial_nature.code,
        esocial_nature_description=rubric.esocial_nature.description,
        is_salary_nature=rubric.esocial_nature.is_salary_nature,
        inss=incidence.inss,
        fgts=incidence.fgts,
        irrf=incidence.irrf,
        iss=incidence.iss,
        inss_observation=incidence.inss_observation,
        fgts_observation=incidence.fgts_observation,
        irrf_observation=incidence.irrf_observation,
        iss_observation=incidence.iss_observation,
        risk_level=incidence.risk_level,
        risk_reason=incidence.risk_reason,
        recently_changed=incidence.recently_changed,
        change_note=incidence.change_note,
        change_date=str(incidence.change_date) if incidence.change_date else None,
        explanation=explanation,
        legal_basis=legal_basis_results,
        contextual_rules_applied=rules_applied,
    )


def search_rubrics(query: str, limit: int = 20):
    """
    Busca rubricas pelo nome usando similaridade trigrama do PostgreSQL.
    Em SQLite (desenvolvimento), faz um LIKE simples.
    """
    from apps.catalog.models import Rubric
    from django.db import connection

    qs = Rubric.objects.filter(is_published=True).select_related(
        'category', 'esocial_nature', 'incidence'
    )

    if connection.vendor == 'postgresql':
        from django.contrib.postgres.search import TrigramSimilarity
        from django.db.models import Q

        # Busca exata por código da natureza eSocial (ex: "6001")
        if query.strip().isdigit():
            return qs.filter(
                Q(esocial_nature__code=query.strip()) |
                Q(esocial_nature__code__startswith=query.strip())
            )[:limit]

        return (
            qs.annotate(similarity=TrigramSimilarity('name', query))
            .filter(similarity__gt=0.1)
            .order_by('-similarity')[:limit]
        )

    # Fallback para SQLite em desenvolvimento
    # Busca tanto por nome quanto por slug (slug não tem acentos)
    from django.db.models import Q

    # Busca por código da natureza eSocial (ex: "6001")
    if query.strip().isdigit():
        return qs.filter(
            Q(esocial_nature__code=query.strip()) |
            Q(esocial_nature__code__startswith=query.strip())
        )[:limit]

    return qs.filter(
        Q(name__icontains=query) | Q(slug__icontains=query)
    )[:limit]


def lookup_esocial_nature(code: str):
    """
    Busca uma natureza eSocial pelo código exato.
    Retorna o objeto EsocialNature ou None.
    """
    from apps.catalog.models import EsocialNature

    return EsocialNature.objects.filter(code=code.strip()).first()


def _apply_contextual_rules(rubric, incidence, context: dict):
    """
    Aplica regras contextuais sobre a incidência base.
    Retorna a incidência modificada e a lista de regras aplicadas.
    """
    from apps.engine.models import ContextualRule
    import copy

    rules = ContextualRule.objects.filter(rubric=rubric)
    modified = copy.copy(incidence)
    applied = []

    for rule in rules:
        context_value = context.get(rule.condition_key)
        if context_value and str(context_value).lower() == rule.condition_value.lower():
            if rule.override_inss is not None:
                modified.inss = rule.override_inss
            if rule.override_fgts is not None:
                modified.fgts = rule.override_fgts
            if rule.override_irrf is not None:
                modified.irrf = rule.override_irrf
            applied.append(rule.condition_description)

    return modified, applied
