"""
Popula o banco com dados iniciais essenciais:
- Naturezas eSocial mais comuns
- Categorias de rubrica
- 10 rubricas mais consultadas no DP, com incidências e base legal
"""
from django.core.management.base import BaseCommand
from django.db import transaction


# Naturezas eSocial agora são gerenciadas pelo comando seed_official_natures.
# Execute: python manage.py seed_official_natures (antes deste seed)

CATEGORIES = [
    {'name': 'Proventos', 'slug': 'proventos', 'category_type': 'provento'},
    {'name': 'Descontos', 'slug': 'descontos', 'category_type': 'desconto'},
    {'name': 'Informativos', 'slug': 'informativos', 'category_type': 'informativo'},
    {'name': 'Bases de Cálculo', 'slug': 'bases-de-calculo', 'category_type': 'base'},
]

LEGAL_NORMS = [
    {
        'norm_type': 'clt', 'number': 'Decreto-Lei 5.452', 'year': 1943,
        'title': 'Consolidação das Leis do Trabalho - CLT',
        'official_link': 'https://www.planalto.gov.br/ccivil_03/decreto-lei/del5452.htm',
    },
    {
        'norm_type': 'lei', 'number': '8.212', 'year': 1991,
        'title': 'Lei Orgânica da Seguridade Social',
        'official_link': 'https://www.planalto.gov.br/ccivil_03/leis/l8212cons.htm',
    },
    {
        'norm_type': 'lei', 'number': '8.036', 'year': 1990,
        'title': 'Lei do FGTS',
        'official_link': 'https://www.planalto.gov.br/ccivil_03/leis/l8036consol.htm',
    },
    {
        'norm_type': 'decreto', 'number': '3.048', 'year': 1999,
        'title': 'Regulamento da Previdência Social',
        'official_link': 'https://www.planalto.gov.br/ccivil_03/decreto/d3048.htm',
    },
    {
        'norm_type': 'lei', 'number': '7.418', 'year': 1985,
        'title': 'Lei do Vale-Transporte',
        'official_link': 'https://www.planalto.gov.br/ccivil_03/leis/l7418.htm',
    },
]

RUBRICAS_SEED = [
    {
        'name': 'Salário Base',
        'code': 'SAL001',
        'description': 'Remuneração mensal base do empregado conforme contrato de trabalho.',
        'category': 'Proventos',
        'esocial_nature_code': '1000',
        'incidence': {'inss': True, 'fgts': True, 'irrf': True, 'risk_level': 'low'},
        'legal_basis': [
            {
                'norm_number': '8.212', 'norm_year': 1991, 'article': 'Art. 28', 'is_primary': True,
                'excerpt': (
                    'Entende-se por salário de contribuição para o empregado e trabalhador avulso: '
                    'I - a remuneração auferida em uma ou mais empresas, assim entendida a totalidade '
                    'dos rendimentos pagos, devidos ou creditados a qualquer título, durante o mês.'
                ),
            }
        ],
    },
    {
        'name': 'Hora Extra 50%',
        'code': 'HE050',
        'description': 'Horas trabalhadas além da jornada normal com adicional mínimo de 50%.',
        'category': 'Proventos',
        'esocial_nature_code': '1003',
        'incidence': {'inss': True, 'fgts': True, 'irrf': True, 'risk_level': 'low'},
        'legal_basis': [
            {
                'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943, 'article': 'Art. 59', 'is_primary': True,
                'excerpt': (
                    'A duração normal do trabalho poderá ser acrescida de horas suplementares, '
                    'em número não excedente de 2 (duas), mediante acordo escrito entre empregador e empregado.'
                ),
            }
        ],
    },
    {
        'name': 'Adicional Noturno',
        'code': 'ANT001',
        'description': 'Adicional de 20% sobre a hora normal para trabalho entre 22h e 5h.',
        'category': 'Proventos',
        'esocial_nature_code': '1205',
        'incidence': {'inss': True, 'fgts': True, 'irrf': True, 'risk_level': 'low'},
        'legal_basis': [
            {
                'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943, 'article': 'Art. 73', 'is_primary': True,
                'excerpt': (
                    'Salvo nos casos de revezamento semanal ou quinzenal, o trabalho noturno terá remuneração '
                    'superior à do diurno e, para esse efeito, sua remuneração terá um acréscimo de 20%.'
                ),
            }
        ],
    },
    {
        'name': 'Férias Gozadas',
        'code': 'FER001',
        'description': 'Pagamento das férias anuais do empregado no período de gozo.',
        'category': 'Proventos',
        'esocial_nature_code': '1016',
        'incidence': {
            'inss': False, 'fgts': False, 'irrf': True,
            'irrf_observation': 'Incide IRRF na competência do pagamento.',
            'risk_level': 'medium',
        },
        'legal_basis': [
            {
                'norm_number': '8.212', 'norm_year': 1991, 'article': 'Art. 28, §9º, d', 'is_primary': True,
                'excerpt': (
                    'Não integram o salário de contribuição: d) as importâncias recebidas a título de '
                    'férias indenizadas e respectivo adicional constitucional.'
                ),
            }
        ],
    },
    {
        'name': 'Adicional 1/3 de Férias',
        'code': 'TFE001',
        'description': 'Adicional constitucional de 1/3 sobre o valor das férias.',
        'category': 'Proventos',
        'esocial_nature_code': '1017',
        'incidence': {
            'inss': False, 'fgts': False, 'irrf': True,
            'irrf_observation': 'Incide IRRF conforme Súmula 463 do TST.',
            'risk_level': 'high',
            'recently_changed': True,
            'change_note': (
                'Súmula 463 do TST consolidou a incidência de IRRF sobre o terço constitucional de férias.'
            ),
        },
        'legal_basis': [
            {
                'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943, 'article': 'Art. 142', 'is_primary': True,
                'excerpt': (
                    'O empregado perceberá, durante as férias, a remuneração que lhe for devida '
                    'na data de sua concessão.'
                ),
            }
        ],
    },
    {
        'name': 'Vale-Transporte (Desconto)',
        'code': 'VTD001',
        'description': 'Desconto do benefício de vale-transporte, limitado a 6% do salário base.',
        'category': 'Descontos',
        'esocial_nature_code': '9216',
        'incidence': {'inss': False, 'fgts': False, 'irrf': False, 'risk_level': 'low'},
        'legal_basis': [
            {
                'norm_number': '7.418', 'norm_year': 1985, 'article': 'Art. 4º', 'is_primary': True,
                'excerpt': (
                    'A concessão do benefício ora instituído implica a aquisição pelo empregador dos '
                    'Vales-Transporte necessários aos deslocamentos do trabalhador.'
                ),
            }
        ],
    },
    {
        'name': '13º Salário (Parcela Final)',
        'code': '13S002',
        'description': 'Segunda parcela da gratificação natalina, paga até 20 de dezembro.',
        'category': 'Proventos',
        'esocial_nature_code': '5001',
        'incidence': {
            'inss': True, 'fgts': True, 'irrf': True,
            'inss_observation': 'O INSS é calculado separadamente do salário mensal.',
            'risk_level': 'low',
        },
        'legal_basis': [
            {
                'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943, 'article': 'Art. 7º, VIII CF/88',
                'is_primary': True,
                'excerpt': (
                    'São direitos dos trabalhadores urbanos e rurais: XIII - décimo terceiro salário '
                    'com base na remuneração integral ou no valor da aposentadoria.'
                ),
            }
        ],
    },
    {
        'name': 'Adicional de Insalubridade',
        'code': 'INS001',
        'description': 'Adicional a que faz jus o empregado exposto a agentes insalubres.',
        'category': 'Proventos',
        'esocial_nature_code': '1202',
        'incidence': {'inss': True, 'fgts': True, 'irrf': True, 'risk_level': 'low'},
        'legal_basis': [
            {
                'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943, 'article': 'Art. 192', 'is_primary': True,
                'excerpt': (
                    'O exercício de trabalho em condições insalubres, acima dos limites de tolerância '
                    'estabelecidos pelo Ministério do Trabalho, assegura a percepção de adicional '
                    'respectivamente de 40%, 20% e 10% do salário-mínimo da região.'
                ),
            }
        ],
    },
    {
        'name': 'Salário-Família',
        'code': 'SFM001',
        'description': 'Benefício pago ao empregado de baixa renda por cada filho de até 14 anos.',
        'category': 'Proventos',
        'esocial_nature_code': '1409',
        'incidence': {'inss': False, 'fgts': False, 'irrf': False, 'risk_level': 'low'},
        'legal_basis': [
            {
                'norm_number': '8.212', 'norm_year': 1991, 'article': 'Art. 28, §9º, j', 'is_primary': True,
                'excerpt': 'Não integram o salário de contribuição: j) o salário-família.',
            }
        ],
    },
    {
        'name': 'Adiantamento Salarial',
        'code': 'ADT001',
        'description': 'Adiantamento do salário pago antes da data regular de pagamento.',
        'category': 'Proventos',
        'esocial_nature_code': '5501',
        'incidence': {
            'inss': False, 'fgts': False, 'irrf': False,
            'inss_observation': 'Não incide no adiantamento. O INSS é calculado no fechamento da folha.',
            'risk_level': 'low',
        },
        'legal_basis': [
            {
                'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943, 'article': 'Art. 459', 'is_primary': True,
                'excerpt': (
                    'O pagamento do salário, qualquer que seja a modalidade do trabalho, '
                    'não deve ser estipulado por período superior a 1 (um) mês.'
                ),
            }
        ],
    },
]


class Command(BaseCommand):
    help = 'Popula o banco com dados iniciais de naturezas eSocial, categorias e rubricas'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        from apps.catalog.models import Category, EsocialNature, Rubric
        from apps.legislation.models import LegalNorm, LegalBasis
        from apps.engine.models import Incidence

        # Naturezas eSocial são gerenciadas pelo comando seed_official_natures
        # Execute: python manage.py seed_official_natures (antes deste seed)

        self.stdout.write('Criando categorias...')
        for data in CATEGORIES:
            Category.objects.get_or_create(slug=data['slug'], defaults=data)

        self.stdout.write('Criando normas legais...')
        norm_map = {}
        for data in LEGAL_NORMS:
            norm, _ = LegalNorm.objects.get_or_create(
                number=data['number'],
                year=data['year'],
                defaults=data
            )
            norm_map[(data['number'], data['year'])] = norm

        self.stdout.write('Criando rubricas e incidências...')
        for r in RUBRICAS_SEED:
            category = Category.objects.get(name=r['category'])
            nature = EsocialNature.objects.filter(code=r['esocial_nature_code']).first()

            rubric, created = Rubric.objects.get_or_create(
                code=r['code'],
                defaults={
                    'name': r['name'],
                    'description': r['description'],
                    'category': category,
                    'esocial_nature': nature,
                    'is_published': True,
                }
            )

            inc_data = r['incidence']
            Incidence.objects.get_or_create(
                rubric=rubric,
                defaults={
                    'inss': inc_data['inss'],
                    'fgts': inc_data['fgts'],
                    'irrf': inc_data['irrf'],
                    'inss_observation': inc_data.get('inss_observation', ''),
                    'fgts_observation': inc_data.get('fgts_observation', ''),
                    'irrf_observation': inc_data.get('irrf_observation', ''),
                    'risk_level': inc_data.get('risk_level', 'low'),
                    'recently_changed': inc_data.get('recently_changed', False),
                    'change_note': inc_data.get('change_note', ''),
                }
            )

            for lb_data in r.get('legal_basis', []):
                norm = norm_map.get((lb_data['norm_number'], lb_data['norm_year']))
                if norm:
                    LegalBasis.objects.get_or_create(
                        rubric=rubric,
                        norm=norm,
                        article=lb_data.get('article', ''),
                        defaults={
                            'excerpt': lb_data.get('excerpt', ''),
                            'is_primary': lb_data.get('is_primary', False),
                        }
                    )

            status_str = 'criada' if created else 'ja existia'
            self.stdout.write(f'  {rubric.name} — {status_str}')

        self.stdout.write(self.style.SUCCESS('\nDados iniciais carregados com sucesso!'))
        self.stdout.write(f'  {Rubric.objects.count()} rubricas no banco')
        self.stdout.write(f'  {Incidence.objects.count()} incidencias cadastradas')
