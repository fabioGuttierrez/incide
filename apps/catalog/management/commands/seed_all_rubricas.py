"""
Seed completo: ~50 rubricas mais consultadas no Departamento Pessoal.
Execute com: python manage.py seed_all_rubricas
"""
from django.core.management.base import BaseCommand
from django.db import transaction

ADDITIONAL_NATURES = [
    {'code': '1090', 'description': 'Sobreaviso e Prontidão', 'is_salary_nature': True},
    {'code': '1100', 'description': 'Adicional de Transferência', 'is_salary_nature': True},
    {'code': '1110', 'description': 'Gratificações e Prêmios', 'is_salary_nature': True},
    {'code': '1140', 'description': 'DSR sobre Horas Extras', 'is_salary_nature': True},
    {'code': '1200', 'description': 'Participação nos Lucros e Resultados (PLR)', 'is_salary_nature': False},
    {'code': '1210', 'description': 'Ajuda de Custo', 'is_salary_nature': False},
    {'code': '1230', 'description': 'Diárias para Viagem', 'is_salary_nature': False},
    {'code': '1300', 'description': 'Aviso Prévio Trabalhado', 'is_salary_nature': True},
    {'code': '1302', 'description': 'Aviso Prévio Indenizado', 'is_salary_nature': False},
    {'code': '1350', 'description': 'Saldo de Salário Rescisório', 'is_salary_nature': True},
    {'code': '1351', 'description': 'Indenização por Tempo de Serviço', 'is_salary_nature': False},
    {'code': '1503', 'description': 'Férias Indenizadas', 'is_salary_nature': False},
    {'code': '5001', 'description': 'Benefício - Vale-Refeição / Alimentação', 'is_salary_nature': False},
    {'code': '5002', 'description': 'Benefício - Plano de Saúde', 'is_salary_nature': False},
    {'code': '5003', 'description': 'Benefício - Auxílio Creche', 'is_salary_nature': False},
    {'code': '5010', 'description': 'Cesta Básica / Auxílio Alimentação PAT', 'is_salary_nature': False},
    {'code': '5050', 'description': 'Seguro de Vida em Grupo', 'is_salary_nature': False},
    {'code': '9220', 'description': 'Plano de Saúde - Desconto Empregado', 'is_salary_nature': False},
    {'code': '9250', 'description': 'Pensão Alimentícia', 'is_salary_nature': False},
    {'code': '9900', 'description': 'Multa FGTS 40%', 'is_salary_nature': False},
]

ADDITIONAL_NORMS = [
    {
        'norm_type': 'lei', 'number': '10.101', 'year': 2000,
        'title': 'Participação dos Trabalhadores nos Lucros ou Resultados da Empresa',
        'official_link': 'https://www.planalto.gov.br/ccivil_03/leis/l10101.htm',
    },
    {
        'norm_type': 'lei', 'number': '6.321', 'year': 1976,
        'title': 'Programa de Alimentação do Trabalhador (PAT)',
        'official_link': 'https://www.planalto.gov.br/ccivil_03/leis/l6321.htm',
    },
    {
        'norm_type': 'decreto', 'number': '95.247', 'year': 1987,
        'title': 'Regulamenta a Lei do Vale-Transporte',
        'official_link': 'https://www.planalto.gov.br/ccivil_03/decreto/d95247.htm',
    },
    {
        'norm_type': 'in_rfb', 'number': '2.141', 'year': 2023,
        'title': 'Instrução Normativa RFB 2.141/2023 — IRRF e contribuições previdenciárias',
        'official_link': 'https://www.in.gov.br/web/dou/-/instrucao-normativa-rfb-n-2.141-de-2-de-junho-de-2023',
    },
    {
        'norm_type': 'lei', 'number': '9.250', 'year': 1995,
        'title': 'Lei 9.250/1995 — IRRF Pessoa Física',
        'official_link': 'https://www.planalto.gov.br/ccivil_03/leis/l9250.htm',
    },
]

RUBRICAS_ADICIONAIS = [
    # ─── Proventos salariais ───────────────────────────────────────────────────
    {
        'name': 'Hora Extra 100%',
        'code': 'HE100',
        'description': 'Horas extras em domingos, feriados ou mediante acordo, com adicional de 100%.',
        'category': 'Proventos',
        'esocial_nature_code': '1040',
        'incidence': {'inss': True, 'fgts': True, 'irrf': True, 'risk_level': 'low'},
        'legal_basis': [
            {
                'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943,
                'article': 'Art. 59, §2º e CF/88 Art. 7º, XVI', 'is_primary': True,
                'excerpt': (
                    'O adicional de horas extras deve ser de no mínimo 50% sobre a hora normal, '
                    'podendo ser de 100% por força de convenção coletiva ou em domingos e feriados.'
                ),
            }
        ],
    },
    {
        'name': 'Adicional de Periculosidade',
        'code': 'PER001',
        'description': 'Adicional de 30% sobre o salário para empregados expostos a atividades perigosas.',
        'category': 'Proventos',
        'esocial_nature_code': '1070',
        'incidence': {'inss': True, 'fgts': True, 'irrf': True, 'risk_level': 'low'},
        'legal_basis': [
            {
                'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943,
                'article': 'Art. 193', 'is_primary': True,
                'excerpt': (
                    'São consideradas atividades ou operações perigosas, na forma da regulamentação '
                    'aprovada pelo Ministério do Trabalho, aquelas que, por sua natureza ou métodos de '
                    'trabalho, impliquem risco acentuado em virtude de exposição permanente do trabalhador a '
                    'inflamáveis, explosivos ou energia elétrica.'
                ),
            }
        ],
    },
    {
        'name': 'Comissões',
        'code': 'COM001',
        'description': 'Remuneração variável paga ao empregado sobre vendas ou negócios realizados.',
        'category': 'Proventos',
        'esocial_nature_code': '1080',
        'incidence': {'inss': True, 'fgts': True, 'irrf': True, 'risk_level': 'low'},
        'legal_basis': [
            {
                'norm_number': '8.212', 'norm_year': 1991,
                'article': 'Art. 28', 'is_primary': True,
                'excerpt': (
                    'O salário de contribuição compreende a totalidade dos rendimentos pagos, devidos '
                    'ou creditados a qualquer título, incluindo as comissões.'
                ),
            }
        ],
    },
    {
        'name': 'Gratificação de Função',
        'code': 'GFN001',
        'description': 'Gratificação paga ao empregado pelo exercício de função de chefia ou confiança.',
        'category': 'Proventos',
        'esocial_nature_code': '1110',
        'incidence': {'inss': True, 'fgts': True, 'irrf': True, 'risk_level': 'low'},
        'legal_basis': [
            {
                'norm_number': '8.212', 'norm_year': 1991,
                'article': 'Art. 28', 'is_primary': True,
                'excerpt': (
                    'Integra o salário de contribuição a totalidade dos rendimentos pagos a qualquer título, '
                    'incluindo gratificações de natureza habitual.'
                ),
            }
        ],
    },
    {
        'name': 'DSR sobre Horas Extras',
        'code': 'DSR001',
        'description': 'Reflexo das horas extras sobre o Descanso Semanal Remunerado.',
        'category': 'Proventos',
        'esocial_nature_code': '1140',
        'incidence': {'inss': True, 'fgts': True, 'irrf': True, 'risk_level': 'medium',
                      'inss_observation': 'Integra a base de cálculo por ser reflexo de verba salarial.'},
        'legal_basis': [
            {
                'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943,
                'article': 'Art. 67 c/c Súmula 172 TST', 'is_primary': True,
                'excerpt': (
                    'Computam-se no cálculo do repouso remunerado as horas extras habitualmente prestadas '
                    '(Súmula 172, TST).'
                ),
            }
        ],
    },
    {
        'name': 'Adicional de Sobreaviso',
        'code': 'SOB001',
        'description': 'Adicional de 1/3 do valor da hora normal pago ao empregado em sobreaviso.',
        'category': 'Proventos',
        'esocial_nature_code': '1090',
        'incidence': {'inss': True, 'fgts': True, 'irrf': True, 'risk_level': 'medium'},
        'legal_basis': [
            {
                'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943,
                'article': 'Art. 244, §2º', 'is_primary': True,
                'excerpt': (
                    'Considera-se de sobreaviso o empregado efetivo, que permanecer em sua própria casa, '
                    'aguardando a qualquer momento o chamado para o serviço. Cada escala de sobreaviso será, '
                    'no máximo, de vinte e quatro horas, e remunerado a 1/3 (um terço) da hora normal.'
                ),
            }
        ],
    },
    {
        'name': 'Adicional de Transferência',
        'code': 'TRF001',
        'description': 'Adicional de 25% sobre o salário devido ao empregado transferido provisoriamente.',
        'category': 'Proventos',
        'esocial_nature_code': '1100',
        'incidence': {'inss': True, 'fgts': True, 'irrf': True, 'risk_level': 'low'},
        'legal_basis': [
            {
                'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943,
                'article': 'Art. 469, §3º', 'is_primary': True,
                'excerpt': (
                    'Em caso de necessidade de serviço o empregador poderá transferir o empregado para '
                    'localidade diversa da que resultar do contrato, não obstante as restrições do artigo '
                    'anterior, mas, nesse caso, ficará obrigado a um pagamento suplementar, nunca inferior '
                    'a 25% dos salários que o empregado percebia naquela localidade.'
                ),
            }
        ],
    },

    # ─── 13º Salário ──────────────────────────────────────────────────────────
    {
        'name': '13º Salário (1ª Parcela)',
        'code': '13S001',
        'description': 'Adiantamento da primeira parcela do 13º salário, pago até 30 de novembro.',
        'category': 'Proventos',
        'esocial_nature_code': '1320',
        'incidence': {
            'inss': False, 'fgts': True, 'irrf': False,
            'inss_observation': 'INSS não incide na 1ª parcela. Incide apenas na 2ª parcela.',
            'irrf_observation': 'IRRF não incide no adiantamento. Incide apenas na 2ª parcela.',
            'risk_level': 'high',
        },
        'legal_basis': [
            {
                'norm_number': '8.212', 'norm_year': 1991,
                'article': 'Art. 28, §7º', 'is_primary': True,
                'excerpt': (
                    'O décimo terceiro salário, na forma estabelecida em lei ou norma coletiva de trabalho, '
                    'integra o salário de contribuição, exceto quando pago como adiantamento da primeira parcela.'
                ),
            }
        ],
    },

    # ─── Férias ────────────────────────────────────────────────────────────────
    {
        'name': 'Férias Indenizadas',
        'code': 'FEI001',
        'description': 'Férias não gozadas indenizadas na rescisão do contrato de trabalho.',
        'category': 'Proventos',
        'esocial_nature_code': '1503',
        'incidence': {
            'inss': False, 'fgts': False, 'irrf': False,
            'risk_level': 'high',
            'recently_changed': True,
            'change_note': (
                'A partir de 2023, férias indenizadas na rescisão são isentas de IRRF '
                'conforme posicionamento consolidado pelo STJ.'
            ),
        },
        'legal_basis': [
            {
                'norm_number': '8.212', 'norm_year': 1991,
                'article': 'Art. 28, §9º, d', 'is_primary': True,
                'excerpt': (
                    'Não integram o salário de contribuição: d) as importâncias recebidas a título de '
                    'férias indenizadas e respectivo adicional constitucional.'
                ),
            }
        ],
    },
    {
        'name': 'Adicional 1/3 Férias Indenizadas',
        'code': 'TFI001',
        'description': 'Terço constitucional sobre férias indenizadas na rescisão.',
        'category': 'Proventos',
        'esocial_nature_code': '1503',
        'incidence': {'inss': False, 'fgts': False, 'irrf': False, 'risk_level': 'medium'},
        'legal_basis': [
            {
                'norm_number': '8.212', 'norm_year': 1991,
                'article': 'Art. 28, §9º, d', 'is_primary': True,
                'excerpt': (
                    'Não integram o salário de contribuição as importâncias recebidas a título de '
                    'férias indenizadas e respectivo adicional constitucional.'
                ),
            }
        ],
    },
    {
        'name': 'Abono Pecuniário de Férias',
        'code': 'APF001',
        'description': 'Conversão de 1/3 das férias em abono pecuniário (dinheiro), a pedido do empregado.',
        'category': 'Proventos',
        'esocial_nature_code': '1501',
        'incidence': {
            'inss': False, 'fgts': False, 'irrf': False,
            'inss_observation': 'Verba indenizatória, não integra o salário de contribuição.',
            'risk_level': 'low',
        },
        'legal_basis': [
            {
                'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943,
                'article': 'Art. 143', 'is_primary': True,
                'excerpt': (
                    'É facultado ao empregado converter 1/3 (um terço) do período de férias a que '
                    'tiver direito em abono pecuniário, no valor da remuneração que lhe seria devida '
                    'nos dias correspondentes.'
                ),
            }
        ],
    },

    # ─── Verbas rescisórias ────────────────────────────────────────────────────
    {
        'name': 'Aviso Prévio Trabalhado',
        'code': 'APT001',
        'description': 'Período de aviso prévio cumprido pelo empregado antes da rescisão.',
        'category': 'Proventos',
        'esocial_nature_code': '1300',
        'incidence': {'inss': True, 'fgts': True, 'irrf': True, 'risk_level': 'low'},
        'legal_basis': [
            {
                'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943,
                'article': 'Art. 487', 'is_primary': True,
                'excerpt': (
                    'Não sendo o prazo de aviso prévio respeitado pelo empregador, o empregado '
                    'poderá requerer a indenização correspondente.'
                ),
            }
        ],
    },
    {
        'name': 'Aviso Prévio Indenizado',
        'code': 'API001',
        'description': 'Indenização pelo aviso prévio não trabalhado, pago pelo empregador na dispensa.',
        'category': 'Proventos',
        'esocial_nature_code': '1302',
        'incidence': {
            'inss': False, 'fgts': True, 'irrf': False,
            'fgts_observation': 'O FGTS incide sobre o aviso prévio indenizado conforme Súmula 305 do TST.',
            'irrf_observation': 'Isento de IRRF por possuir natureza indenizatória.',
            'risk_level': 'high',
        },
        'legal_basis': [
            {
                'norm_number': '8.036', 'norm_year': 1990,
                'article': 'Art. 15, §6º', 'is_primary': True,
                'excerpt': (
                    'O FGTS incidirá sobre o valor do aviso prévio indenizado, '
                    'conforme Súmula 305 do Tribunal Superior do Trabalho.'
                ),
            }
        ],
    },
    {
        'name': 'Saldo de Salário Rescisório',
        'code': 'SSR001',
        'description': 'Salário proporcional aos dias trabalhados no mês da rescisão.',
        'category': 'Proventos',
        'esocial_nature_code': '1350',
        'incidence': {'inss': True, 'fgts': True, 'irrf': True, 'risk_level': 'low'},
        'legal_basis': [
            {
                'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943,
                'article': 'Art. 477', 'is_primary': True,
                'excerpt': (
                    'Na extinção do contrato de trabalho, o empregador deverá proceder à anotação '
                    'na Carteira de Trabalho e Previdência Social, comunicar a dispensa aos órgãos '
                    'competentes e realizar o pagamento das verbas rescisórias.'
                ),
            }
        ],
    },
    {
        'name': 'Multa FGTS 40%',
        'code': 'MUL001',
        'description': 'Multa de 40% sobre o saldo do FGTS devida ao empregado dispensado sem justa causa.',
        'category': 'Proventos',
        'esocial_nature_code': '9900',
        'incidence': {'inss': False, 'fgts': False, 'irrf': False, 'risk_level': 'low'},
        'legal_basis': [
            {
                'norm_number': '8.036', 'norm_year': 1990,
                'article': 'Art. 18, §1º', 'is_primary': True,
                'excerpt': (
                    'Na hipótese de dispensa pelo empregador sem justa causa, depositará este, na conta '
                    'vinculada do trabalhador no FGTS, importância igual a quarenta por cento do '
                    'montante de todos os depósitos realizados na conta vinculada durante a '
                    'vigência do contrato de trabalho.'
                ),
            }
        ],
    },
    {
        'name': 'Indenização por Tempo de Serviço',
        'code': 'IND001',
        'description': 'Indenização paga a empregados estáveis dispensados antes da vigência do FGTS.',
        'category': 'Proventos',
        'esocial_nature_code': '1351',
        'incidence': {'inss': False, 'fgts': False, 'irrf': False, 'risk_level': 'low'},
        'legal_basis': [
            {
                'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943,
                'article': 'Art. 477', 'is_primary': True,
                'excerpt': (
                    'Verbas indenizatórias pagas na rescisão contratual não integram o salário '
                    'de contribuição nem a base de cálculo do IRRF.'
                ),
            }
        ],
    },

    # ─── Benefícios ────────────────────────────────────────────────────────────
    {
        'name': 'Vale-Refeição / Alimentação (Benefício)',
        'code': 'VRF001',
        'description': 'Fornecimento de vale-refeição ou alimentação ao empregado como benefício.',
        'category': 'Proventos',
        'esocial_nature_code': '5001',
        'incidence': {
            'inss': False, 'fgts': False, 'irrf': False,
            'inss_observation': 'Não incide desde que vinculado ao PAT (Programa de Alimentação do Trabalhador).',
            'risk_level': 'medium',
        },
        'legal_basis': [
            {
                'norm_number': '6.321', 'norm_year': 1976,
                'article': 'Art. 3º', 'is_primary': True,
                'excerpt': (
                    'Nos termos da legislação que rege o PAT, as despesas com o programa de '
                    'alimentação do trabalhador não se constituem base de incidência de '
                    'contribuição previdenciária ou FGTS.'
                ),
            }
        ],
    },
    {
        'name': 'Cesta Básica / Auxílio Alimentação (PAT)',
        'code': 'CEB001',
        'description': 'Fornecimento de cesta básica ou auxílio alimentação vinculado ao PAT.',
        'category': 'Proventos',
        'esocial_nature_code': '5010',
        'incidence': {
            'inss': False, 'fgts': False, 'irrf': False,
            'inss_observation': 'Não incide quando o programa está devidamente registrado no PAT.',
            'risk_level': 'medium',
        },
        'legal_basis': [
            {
                'norm_number': '6.321', 'norm_year': 1976,
                'article': 'Art. 3º', 'is_primary': True,
                'excerpt': (
                    'Benefícios de alimentação concedidos no âmbito do PAT estão isentos de '
                    'contribuição previdenciária e FGTS.'
                ),
            }
        ],
    },
    {
        'name': 'Plano de Saúde (Benefício Empresa)',
        'code': 'PLS001',
        'description': 'Custeio de plano de saúde pela empresa em favor do empregado e dependentes.',
        'category': 'Proventos',
        'esocial_nature_code': '5002',
        'incidence': {
            'inss': False, 'fgts': False, 'irrf': False,
            'inss_observation': 'Não incide quando o benefício é extensível a todos os empregados.',
            'risk_level': 'medium',
        },
        'legal_basis': [
            {
                'norm_number': '8.212', 'norm_year': 1991,
                'article': 'Art. 28, §9º, q', 'is_primary': True,
                'excerpt': (
                    'Não integram o salário de contribuição o valor das contribuições efetivamente '
                    'pago pela pessoa jurídica relativo a programa de previdência complementar, '
                    'aberto ou fechado, de que trata a Lei n. 9.477, de 24 de julho de 1997.'
                ),
            }
        ],
    },
    {
        'name': 'Auxílio Creche',
        'code': 'AUX001',
        'description': 'Ressarcimento de despesas com creche ou pré-escola para filhos do empregado.',
        'category': 'Proventos',
        'esocial_nature_code': '5003',
        'incidence': {'inss': False, 'fgts': False, 'irrf': False, 'risk_level': 'low'},
        'legal_basis': [
            {
                'norm_number': '8.212', 'norm_year': 1991,
                'article': 'Art. 28, §9º, s', 'is_primary': True,
                'excerpt': (
                    'Não integram o salário de contribuição: o ressarcimento de despesas pelo '
                    'uso de veículo do empregado e o auxílio para creche.'
                ),
            }
        ],
    },
    {
        'name': 'Seguro de Vida em Grupo',
        'code': 'SEG001',
        'description': 'Prêmio de seguro de vida em grupo custeado pela empresa.',
        'category': 'Informativos',
        'esocial_nature_code': '5050',
        'incidence': {'inss': False, 'fgts': False, 'irrf': False, 'risk_level': 'low'},
        'legal_basis': [
            {
                'norm_number': '8.212', 'norm_year': 1991,
                'article': 'Art. 28, §9º', 'is_primary': True,
                'excerpt': (
                    'O seguro de vida em grupo não integra o salário de contribuição '
                    'por não possuir natureza salarial.'
                ),
            }
        ],
    },
    {
        'name': 'Auxílio Home Office',
        'code': 'HOM001',
        'description': 'Auxílio pago ao empregado em regime de teletrabalho para custeio de infraestrutura.',
        'category': 'Informativos',
        'esocial_nature_code': '1210',
        'incidence': {
            'inss': False, 'fgts': False, 'irrf': False,
            'inss_observation': (
                'Não incide quando configurado como ressarcimento de despesas comprovadas, '
                'conforme art. 75-D da CLT.'
            ),
            'risk_level': 'medium',
        },
        'legal_basis': [
            {
                'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943,
                'article': 'Art. 75-D', 'is_primary': True,
                'excerpt': (
                    'As disposições relativas à responsabilidade pela aquisição, manutenção ou '
                    'fornecimento dos equipamentos tecnológicos e da infraestrutura necessária e adequada '
                    'à prestação do trabalho remoto serão previstas em contrato escrito.'
                ),
            }
        ],
    },

    # ─── Descontos ─────────────────────────────────────────────────────────────
    {
        'name': 'INSS Segurado',
        'code': 'INSS01',
        'description': 'Desconto da contribuição previdenciária do empregado conforme tabela vigente.',
        'category': 'Descontos',
        'esocial_nature_code': '9001',
        'incidence': {'inss': False, 'fgts': False, 'irrf': False, 'risk_level': 'low'},
        'legal_basis': [
            {
                'norm_number': '8.212', 'norm_year': 1991,
                'article': 'Art. 20', 'is_primary': True,
                'excerpt': (
                    'A contribuição do empregado, inclusive o doméstico, e a do trabalhador avulso '
                    'é calculada mediante a aplicação da correspondente alíquota sobre o seu '
                    'salário de contribuição mensal.'
                ),
            }
        ],
    },
    {
        'name': 'IRRF (Desconto)',
        'code': 'IRRF01',
        'description': 'Retenção do Imposto de Renda Retido na Fonte sobre a remuneração mensal.',
        'category': 'Descontos',
        'esocial_nature_code': '9003',
        'incidence': {'inss': False, 'fgts': False, 'irrf': False, 'risk_level': 'low'},
        'legal_basis': [
            {
                'norm_number': '9.250', 'norm_year': 1995,
                'article': 'Art. 3º', 'is_primary': True,
                'excerpt': (
                    'O imposto de renda incidente sobre os rendimentos de que tratam os arts. '
                    '1º e 2º será calculado com base na tabela progressiva mensal.'
                ),
            }
        ],
    },
    {
        'name': 'Vale-Refeição / Alimentação (Desconto)',
        'code': 'VRD001',
        'description': 'Desconto do vale-refeição ou alimentação fornecido pela empresa (parte do empregado).',
        'category': 'Descontos',
        'esocial_nature_code': '9210',
        'incidence': {'inss': False, 'fgts': False, 'irrf': False, 'risk_level': 'low'},
        'legal_basis': [
            {
                'norm_number': '6.321', 'norm_year': 1976,
                'article': 'Art. 2º', 'is_primary': True,
                'excerpt': (
                    'A participação do trabalhador no custeio do benefício de alimentação '
                    'não tem natureza salarial.'
                ),
            }
        ],
    },
    {
        'name': 'Plano de Saúde (Desconto Empregado)',
        'code': 'PLD001',
        'description': 'Desconto da parcela do plano de saúde de responsabilidade do empregado.',
        'category': 'Descontos',
        'esocial_nature_code': '9220',
        'incidence': {'inss': False, 'fgts': False, 'irrf': False, 'risk_level': 'low'},
        'legal_basis': [
            {
                'norm_number': '8.212', 'norm_year': 1991,
                'article': 'Art. 28, §9º', 'is_primary': True,
                'excerpt': 'O desconto do plano de saúde não integra o salário de contribuição.',
            }
        ],
    },
    {
        'name': 'Pensão Alimentícia',
        'code': 'PEN001',
        'description': 'Desconto judicial de pensão alimentícia conforme ordem/mandado judicial.',
        'category': 'Descontos',
        'esocial_nature_code': '9250',
        'incidence': {'inss': False, 'fgts': False, 'irrf': False, 'risk_level': 'low'},
        'legal_basis': [
            {
                'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943,
                'article': 'Art. 462', 'is_primary': True,
                'excerpt': (
                    'Ao empregador é vedado efetuar qualquer desconto nos salários do empregado, '
                    'salvo quando este resultar de adiantamentos, de dispositivos de lei ou de '
                    'contrato coletivo.'
                ),
            }
        ],
    },

    # ─── Especiais ─────────────────────────────────────────────────────────────
    {
        'name': 'PLR - Participação nos Lucros',
        'code': 'PLR001',
        'description': 'Participação do empregado nos lucros ou resultados da empresa, conforme acordo coletivo.',
        'category': 'Proventos',
        'esocial_nature_code': '1200',
        'incidence': {
            'inss': False, 'fgts': False, 'irrf': True,
            'irrf_observation': (
                'Incide IRRF com tabela progressiva exclusiva de PLR (não acumula com salário). '
                'Alíquota varia de 0% a 27,5% conforme faixas anuais.'
            ),
            'risk_level': 'medium',
        },
        'legal_basis': [
            {
                'norm_number': '10.101', 'norm_year': 2000,
                'article': 'Art. 3º', 'is_primary': True,
                'excerpt': (
                    'A participação nos lucros ou resultados não substitui ou complementa a remuneração '
                    'devida a qualquer empregado, nem constitui base de incidência de qualquer encargo '
                    'trabalhista, não se lhe aplicando o princípio da habitualidade.'
                ),
            }
        ],
    },
    {
        'name': 'Ajuda de Custo',
        'code': 'AJC001',
        'description': 'Pagamento único para cobrir despesas em transferência definitiva de local de trabalho.',
        'category': 'Informativos',
        'esocial_nature_code': '1210',
        'incidence': {
            'inss': False, 'fgts': False, 'irrf': False,
            'inss_observation': (
                'Não incide quando paga em parcela única em razão de transferência definitiva.'
            ),
            'risk_level': 'medium',
        },
        'legal_basis': [
            {
                'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943,
                'article': 'Art. 470', 'is_primary': True,
                'excerpt': (
                    'As despesas resultantes da transferência correrão por conta do empregador. '
                    'A ajuda de custo não integra o salário quando paga em cota única.'
                ),
            }
        ],
    },
    {
        'name': 'Diárias para Viagem',
        'code': 'DIA001',
        'description': 'Valor pago ao empregado para cobertura de despesas em viagem a serviço.',
        'category': 'Informativos',
        'esocial_nature_code': '1230',
        'incidence': {
            'inss': False, 'fgts': False, 'irrf': False,
            'inss_observation': (
                'Não incide quando o total não excede 50% da remuneração mensal do empregado. '
                'Acima desse limite, o excesso integra o salário de contribuição.'
            ),
            'risk_level': 'medium',
        },
        'legal_basis': [
            {
                'norm_number': '8.212', 'norm_year': 1991,
                'article': 'Art. 28, §9º, h', 'is_primary': True,
                'excerpt': (
                    'Não integram o salário de contribuição as diárias para viagens que, '
                    'não excedentes a 50% da remuneração mensal, não sejam auferidas pelo '
                    'empregado de forma habitual.'
                ),
            }
        ],
    },
]


class Command(BaseCommand):
    help = 'Adiciona ~40 rubricas adicionais ao banco (complementa o seed_initial_data)'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        from apps.catalog.models import Category, EsocialNature, Rubric
        from apps.legislation.models import LegalNorm, LegalBasis
        from apps.engine.models import Incidence

        self.stdout.write('Criando naturezas eSocial adicionais...')
        for data in ADDITIONAL_NATURES:
            EsocialNature.objects.get_or_create(
                code=data['code'],
                description=data['description'],
                defaults={'is_salary_nature': data['is_salary_nature']}
            )

        self.stdout.write('Criando normas legais adicionais...')
        norm_map = {}
        # Carrega normas já existentes
        from apps.legislation.models import LegalNorm as LN
        for norm in LN.objects.all():
            norm_map[(norm.number, norm.year)] = norm

        for data in ADDITIONAL_NORMS:
            norm, _ = LegalNorm.objects.get_or_create(
                number=data['number'],
                year=data['year'],
                defaults=data
            )
            norm_map[(data['number'], data['year'])] = norm

        self.stdout.write('Criando rubricas adicionais...')
        created_count = 0
        for r in RUBRICAS_ADICIONAIS:
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

            if created:
                created_count += 1
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

                self.stdout.write(f'  + {rubric.name}')

        self.stdout.write(self.style.SUCCESS(
            f'\n{created_count} rubricas adicionadas. '
            f'Total no banco: {Rubric.objects.count()} rubricas / '
            f'{Incidence.objects.count()} incidencias.'
        ))
