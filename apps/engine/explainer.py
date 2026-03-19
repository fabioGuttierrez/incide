"""
Gerador de explicações automáticas para incidências.

Este módulo transforma dados estruturados em texto técnico legível,
que é o diferencial principal do produto frente a uma simples tabela.
"""

# Mapeamento (inss, fgts, irrf) → template de explicação
EXPLANATION_TEMPLATES = {
    (True, True, True): (
        "{rubric} possui natureza {nature_type} e integra o salário de contribuição. "
        "Por isso, incide INSS (base previdenciária), FGTS (base fundiária) e IRRF "
        "(sujeito à tabela progressiva), conforme {primary_basis}."
    ),
    (True, True, False): (
        "{rubric} possui natureza {nature_type} para fins previdenciários e fundiários. "
        "Incide INSS e FGTS, porém não compõe a base de cálculo do IRRF, "
        "conforme {primary_basis}."
    ),
    (True, False, True): (
        "{rubric} incide INSS e IRRF, mas não compõe a base de cálculo do FGTS. "
        "Consulte a base legal vinculada para fundamentação específica."
    ),
    (True, False, False): (
        "{rubric} possui natureza {nature_type} apenas para fins previdenciários. "
        "Incide exclusivamente INSS, sem reflexo em FGTS ou IRRF, "
        "conforme {primary_basis}."
    ),
    (False, True, False): (
        "{rubric} compõe a base de cálculo do FGTS, porém não incide INSS nem IRRF. "
        "Verifique a base legal vinculada para a fundamentação desta regra."
    ),
    (False, False, True): (
        "{rubric} está sujeita apenas à retenção de IRRF, sem incidência de INSS "
        "ou FGTS. Consulte a base legal para a alíquota e tabela aplicável."
    ),
    (False, False, False): (
        "{rubric} possui caráter {nature_type} e está excluída das bases de "
        "INSS, FGTS e IRRF, conforme {primary_basis}. "
        "O pagamento ocorre sem qualquer desconto previdenciário ou tributário."
    ),
}

FALLBACK_TEMPLATE = (
    "{rubric}: consulte a base legal vinculada para verificar "
    "a fundamentação das incidências aplicáveis."
)


def generate_explanation(rubric, incidence, legal_basis_qs) -> str:
    key = (incidence.inss, incidence.fgts, incidence.irrf)
    template = EXPLANATION_TEMPLATES.get(key, FALLBACK_TEMPLATE)

    primary = next((lb for lb in legal_basis_qs if lb.is_primary), None)
    primary_str = str(primary.norm) if primary else "legislação vigente"

    nature_type = (
        "salarial"
        if rubric.esocial_nature.is_salary_nature
        else "indenizatória"
    )

    return template.format(
        rubric=rubric.name,
        nature_type=nature_type,
        primary_basis=primary_str,
    )
