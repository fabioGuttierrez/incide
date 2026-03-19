"""
Seed v1.1 — 55 rubricas cobrindo:
  - Jornada especial e horas extras avançadas
  - Adicionais e complementos salariais
  - Férias e 13º completos (rescisórios e descontos)
  - Verbas rescisórias avançadas
  - Descontos do empregado
  - Benefícios avançados
  - Bases de cálculo e informativos
  - Regimes especiais (aprendiz, estagiário, doméstico)
  - Licenças e afastamentos

Execute com: python manage.py seed_v11_rubricas
"""
from django.core.management.base import BaseCommand
from django.db import transaction


V11_NATURES = [
    {'code': '1030', 'description': 'Horas in Itinere', 'is_salary_nature': True},
    {'code': '1035', 'description': 'Intervalo Intrajornada Nao Concedido', 'is_salary_nature': True},
    {'code': '1045', 'description': 'Banco de Horas — Saldo Pago', 'is_salary_nature': True},
    {'code': '1115', 'description': 'Gorjetas', 'is_salary_nature': True},
    {'code': '1120', 'description': 'Premio / Bonificacao Habitual', 'is_salary_nature': True},
    {'code': '1130', 'description': 'Gratificacao por Assiduidade', 'is_salary_nature': True},
    {'code': '1135', 'description': 'Bonus Anual', 'is_salary_nature': True},
    {'code': '1305', 'description': 'Aviso Previo Proporcional', 'is_salary_nature': False},
    {'code': '1310', 'description': '13 Salario Rescisorio', 'is_salary_nature': True},
    {'code': '1400', 'description': 'Salario-Maternidade', 'is_salary_nature': True},
    {'code': '1410', 'description': 'Licenca Paternidade', 'is_salary_nature': True},
    {'code': '1420', 'description': 'Auxilio-Doenca Previdenciario (INSS)', 'is_salary_nature': False},
    {'code': '1430', 'description': 'Auxilio-Doenca Acidentario (CAT)', 'is_salary_nature': False},
    {'code': '1505', 'description': 'Ferias Proporcionais Rescisorias', 'is_salary_nature': False},
    {'code': '1510', 'description': 'Adicional 1/3 s/ Ferias Proporcionais Resc.', 'is_salary_nature': False},
    {'code': '1600', 'description': 'Aprendiz — Salario', 'is_salary_nature': True},
    {'code': '1610', 'description': 'Estagiario — Bolsa Auxilio', 'is_salary_nature': False},
    {'code': '1620', 'description': 'Domestico — Salario Base', 'is_salary_nature': True},
    {'code': '5020', 'description': 'Auxilio Educacao / Bolsa de Estudos', 'is_salary_nature': False},
    {'code': '5030', 'description': 'Vale-Combustivel / Auxilio Combustivel', 'is_salary_nature': False},
    {'code': '5040', 'description': 'Previdencia Complementar (Empregador)', 'is_salary_nature': False},
    {'code': '5060', 'description': 'Auxilio Farmacia', 'is_salary_nature': False},
    {'code': '5070', 'description': 'Auxilio Moradia', 'is_salary_nature': False},
    {'code': '9100', 'description': 'FGTS Mensal (Deposito Empresa)', 'is_salary_nature': False},
    {'code': '9110', 'description': 'FGTS sobre 13 Salario', 'is_salary_nature': False},
    {'code': '9120', 'description': 'INSS sobre 13 Salario (Desconto)', 'is_salary_nature': False},
    {'code': '9130', 'description': 'IRRF sobre 13 Salario (Desconto)', 'is_salary_nature': False},
    {'code': '9150', 'description': 'Desconto por Faltas e Atrasos', 'is_salary_nature': False},
    {'code': '9160', 'description': 'DSR sobre Faltas', 'is_salary_nature': False},
    {'code': '9170', 'description': 'Emprestimo Consignado (Desconto)', 'is_salary_nature': False},
    {'code': '9180', 'description': 'Contribuicao Sindical (Facultativa)', 'is_salary_nature': False},
    {'code': '9200', 'description': 'Adiantamento de 13 (Desconto 2a Parcela)', 'is_salary_nature': False},
    {'code': '9910', 'description': 'Multa FGTS 20% (Rescisao Consensual)', 'is_salary_nature': False},
    {'code': '9920', 'description': 'FGTS Rescisorio (Informativo)', 'is_salary_nature': False},
]

V11_NORMS = [
    {
        'norm_type': 'lei', 'number': '8.213', 'year': 1991,
        'title': 'Planos de Beneficios da Previdencia Social',
        'official_link': 'https://www.planalto.gov.br/ccivil_03/leis/l8213cons.htm',
    },
    {
        'norm_type': 'lc', 'number': '150', 'year': 2015,
        'title': 'LC 150/2015 — Empregado Domestico',
        'official_link': 'https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp150.htm',
    },
    {
        'norm_type': 'lei', 'number': '11.788', 'year': 2008,
        'title': 'Lei do Estagio',
        'official_link': 'https://www.planalto.gov.br/ccivil_03/_ato2007-2010/2008/lei/l11788.htm',
    },
    {
        'norm_type': 'lei', 'number': '10.097', 'year': 2000,
        'title': 'Lei do Aprendiz',
        'official_link': 'https://www.planalto.gov.br/ccivil_03/leis/l10097.htm',
    },
    {
        'norm_type': 'lei', 'number': '13.467', 'year': 2017,
        'title': 'Reforma Trabalhista — Lei 13.467/2017',
        'official_link': 'https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2017/lei/l13467.htm',
    },
    {
        'norm_type': 'lei', 'number': '12.506', 'year': 2011,
        'title': 'Lei 12.506/2011 — Aviso Previo Proporcional',
        'official_link': 'https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2011/lei/l12506.htm',
    },
    {
        'norm_type': 'lei', 'number': '9.029', 'year': 1995,
        'title': 'Lei 9.029/1995 — Dispensa Discriminatoria',
        'official_link': 'https://www.planalto.gov.br/ccivil_03/leis/l9029.htm',
    },
    {
        'norm_type': 'lei', 'number': '14.601', 'year': 2023,
        'title': 'Lei 14.601/2023 — Consignado Privado',
        'official_link': 'https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2023/lei/l14601.htm',
    },
]

RUBRICAS_V11 = [

    # ── Jornada especial ──────────────────────────────────────────────────────
    {
        'name': 'Hora Extra em Feriado (100%)',
        'code': 'HEF001',
        'description': 'Trabalho em feriados remunerado com adicional de 100% por norma coletiva ou disposicao legal.',
        'category': 'Proventos',
        'esocial_nature_code': '1040',
        'incidence': {'inss': True, 'fgts': True, 'irrf': True, 'risk_level': 'low'},
        'legal_basis': [{'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943, 'article': 'Art. 70', 'is_primary': True,
            'excerpt': 'Nos feriados civis e religiosos, o empregador pagara ao empregado, quando obrigado a trabalhar, o dobro da remuneracao do dia normal.'}],
    },
    {
        'name': 'DSR sobre Comissoes',
        'code': 'DSC001',
        'description': 'Reflexo das comissoes sobre o Descanso Semanal Remunerado, obrigatorio quando habitual.',
        'category': 'Proventos',
        'esocial_nature_code': '1140',
        'incidence': {'inss': True, 'fgts': True, 'irrf': True, 'risk_level': 'medium',
                      'inss_observation': 'Integra a base de contribuicao por reflexo de verba salarial habitual.'},
        'legal_basis': [{'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943, 'article': 'Art. 67 c/c Sumula 27 TST', 'is_primary': True,
            'excerpt': 'E devida a remuneracao do repouso semanal e dos dias feriados ao empregado comissionista, ainda que pracista.'}],
    },
    {
        'name': 'Banco de Horas — Saldo a Pagar',
        'code': 'BNH001',
        'description': 'Pagamento do saldo positivo de banco de horas nao compensado ate o prazo acordado.',
        'category': 'Proventos',
        'esocial_nature_code': '1045',
        'incidence': {'inss': True, 'fgts': True, 'irrf': True, 'risk_level': 'medium',
                      'inss_observation': 'O saldo pago em dinheiro tem natureza salarial e integra a base de calculo.'},
        'legal_basis': [{'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943, 'article': 'Art. 59, par. 6', 'is_primary': True,
            'excerpt': 'O banco de horas nao compensado dentro do semestre ou do ano, conforme o acordo, devera ser pago como hora extra.'}],
    },
    {
        'name': 'Intervalo Intrajornada Nao Concedido',
        'code': 'INT001',
        'description': 'Pagamento do periodo de intervalo intrajornada suprimido ou reduzido pelo empregador.',
        'category': 'Proventos',
        'esocial_nature_code': '1035',
        'incidence': {'inss': True, 'fgts': True, 'irrf': True, 'risk_level': 'high',
                      'inss_observation': 'Apos Reforma Trabalhista (Lei 13.467/2017), o pagamento e de 50% sobre o periodo suprimido. Ha divergencia sobre encargos — recomenda-se recolher INSS/FGTS para evitar autuacao.'},
        'legal_basis': [{'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943, 'article': 'Art. 71, par. 4', 'is_primary': True,
            'excerpt': 'A nao concessao ou a concessao parcial do intervalo intrajornada minimo implica o pagamento, de natureza indenizatoria, apenas do periodo suprimido, com acrescimo de 50% sobre o valor da hora normal.'}],
    },
    {
        'name': 'Horas in Itinere',
        'code': 'ITI001',
        'description': 'Horas de deslocamento em transporte fornecido pela empresa, extintas pela Reforma Trabalhista para contratos pos-2017.',
        'category': 'Informativos',
        'esocial_nature_code': '1030',
        'incidence': {'inss': False, 'fgts': False, 'irrf': False, 'risk_level': 'high',
                      'inss_observation': 'Extintas pela Reforma Trabalhista (Lei 13.467/2017) para contratos posteriores a nov/2017. Para contratos anteriores, ha divergencia jurisprudencial — verificar caso a caso.'},
        'legal_basis': [{'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943, 'article': 'Art. 58, par. 2', 'is_primary': True,
            'excerpt': 'O tempo despendido pelo empregado desde a sua residencia ate a efetiva ocupacao do posto de trabalho nao sera computado na jornada de trabalho.'}],
    },

    # ── Adicionais e complementos salariais ───────────────────────────────────
    {
        'name': 'Insalubridade — Grau Maximo (40%)',
        'code': 'INS040',
        'description': 'Adicional de insalubridade no grau maximo: 40% sobre o salario minimo, conforme NR-15.',
        'category': 'Proventos',
        'esocial_nature_code': '1060',
        'incidence': {'inss': True, 'fgts': True, 'irrf': True, 'risk_level': 'low'},
        'legal_basis': [{'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943, 'article': 'Art. 192, I', 'is_primary': True,
            'excerpt': 'O exercicio de trabalho em condicoes insalubres, no grau maximo, assegura ao empregado adicional de 40% do salario-minimo da regiao.'}],
    },
    {
        'name': 'Insalubridade — Grau Medio (20%)',
        'code': 'INS020',
        'description': 'Adicional de insalubridade no grau medio: 20% sobre o salario minimo, conforme NR-15.',
        'category': 'Proventos',
        'esocial_nature_code': '1060',
        'incidence': {'inss': True, 'fgts': True, 'irrf': True, 'risk_level': 'low'},
        'legal_basis': [{'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943, 'article': 'Art. 192, II', 'is_primary': True,
            'excerpt': 'O exercicio de trabalho em condicoes insalubres, no grau medio, assegura ao empregado adicional de 20% do salario-minimo da regiao.'}],
    },
    {
        'name': 'Insalubridade — Grau Minimo (10%)',
        'code': 'INS010',
        'description': 'Adicional de insalubridade no grau minimo: 10% sobre o salario minimo, conforme NR-15.',
        'category': 'Proventos',
        'esocial_nature_code': '1060',
        'incidence': {'inss': True, 'fgts': True, 'irrf': True, 'risk_level': 'low'},
        'legal_basis': [{'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943, 'article': 'Art. 192, III', 'is_primary': True,
            'excerpt': 'O exercicio de trabalho em condicoes insalubres, no grau minimo, assegura ao empregado adicional de 10% do salario-minimo da regiao.'}],
    },
    {
        'name': 'Premio de Produtividade',
        'code': 'PRP001',
        'description': 'Valor pago como reconhecimento por desempenho superior ao esperado; nao incide encargos se eventual (ate 2x/ano).',
        'category': 'Proventos',
        'esocial_nature_code': '1120',
        'incidence': {'inss': False, 'fgts': False, 'irrf': True, 'risk_level': 'high',
                      'inss_observation': 'Nao incide INSS/FGTS se pago em carater eventual (ate 2x/ano), conforme Art. 457, par. 4 CLT. Pagamentos habituais passam a ter natureza salarial.',
                      'irrf_observation': 'Incide IRRF independentemente da habitualidade.'},
        'legal_basis': [{'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943, 'article': 'Art. 457, par. 4', 'is_primary': True,
            'excerpt': 'Consideram-se premios as liberalidades concedidas pelo empregador em forma de bens, servicos ou valor em dinheiro a empregado, em razao de desempenho superior ao ordinariamente esperado no exercicio de suas atividades.'}],
    },
    {
        'name': 'Gorjeta',
        'code': 'GOR001',
        'description': 'Valor espontaneamente dado pelo cliente ou cobrado pela empresa como percentual de servico.',
        'category': 'Proventos',
        'esocial_nature_code': '1115',
        'incidence': {'inss': True, 'fgts': True, 'irrf': True, 'risk_level': 'medium',
                      'inss_observation': 'A gorjeta integra o salario de contribuicao conforme Art. 457, par. 3 CLT e Sumula 354 do TST.'},
        'legal_basis': [{'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943, 'article': 'Art. 457, par. 3', 'is_primary': True,
            'excerpt': 'Considera-se gorjeta nao so a importancia espontaneamente dada pelo cliente ao empregado, como tambem o valor cobrado pela empresa, como percentagem sobre as contas, a titulo de servico ou congenere.'}],
    },
    {
        'name': 'Gratificacao por Assiduidade',
        'code': 'GAS001',
        'description': 'Gratificacao paga ao empregado sem faltas ou atrasos; natureza salarial quando habitual.',
        'category': 'Proventos',
        'esocial_nature_code': '1130',
        'incidence': {'inss': True, 'fgts': True, 'irrf': True, 'risk_level': 'medium',
                      'inss_observation': 'Integra o salario de contribuicao quando paga de forma habitual, independentemente do nome dado pelo empregador (Sumula 203 do TST).'},
        'legal_basis': [{'norm_number': '8.212', 'norm_year': 1991, 'article': 'Art. 28', 'is_primary': True,
            'excerpt': 'Integra o salario de contribuicao a totalidade dos rendimentos pagos a qualquer titulo, incluindo gratificacoes de natureza habitual.'}],
    },
    {
        'name': 'Bonus Anual',
        'code': 'BON001',
        'description': 'Pagamento anual de bonus vinculado a metas corporativas, geralmente pago no inicio do ano seguinte.',
        'category': 'Proventos',
        'esocial_nature_code': '1135',
        'incidence': {'inss': True, 'fgts': True, 'irrf': True, 'risk_level': 'high',
                      'inss_observation': 'Se pago habitualmente (todos os anos), incorpora-se ao salario e integra a base de contribuicao. Se eventual, pode ser tratado como premio (Art. 457, par. 4 CLT).'},
        'legal_basis': [{'norm_number': '8.212', 'norm_year': 1991, 'article': 'Art. 28', 'is_primary': True,
            'excerpt': 'Integra o salario de contribuicao a totalidade dos rendimentos pagos, devidos ou creditados a qualquer titulo, durante o mes, destinados a retribuir o trabalho.'}],
    },

    # ── Ferias completo ────────────────────────────────────────────────────────
    {
        'name': 'Ferias Proporcionais Rescisorias',
        'code': 'FPR001',
        'description': 'Ferias proporcionais ao tempo de servico no periodo aquisitivo incompleto, pagas na rescisao.',
        'category': 'Proventos',
        'esocial_nature_code': '1505',
        'incidence': {'inss': False, 'fgts': False, 'irrf': False, 'risk_level': 'medium',
                      'irrf_observation': 'Isentas de IRRF por natureza indenizatoria, conforme posicionamento do STJ e RFB.'},
        'legal_basis': [{'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943, 'article': 'Art. 146 e 147', 'is_primary': True,
            'excerpt': 'Na cessacao do contrato de trabalho, qualquer que seja a sua causa, sera devida ao empregado a remuneracao correspondente ao periodo de ferias cujo direito tenha adquirido.'}],
    },
    {
        'name': 'Adicional 1/3 — Ferias Proporcionais Rescisorias',
        'code': 'TFP001',
        'description': 'Adicional constitucional de 1/3 sobre as ferias proporcionais pagas na rescisao contratual.',
        'category': 'Proventos',
        'esocial_nature_code': '1510',
        'incidence': {'inss': False, 'fgts': False, 'irrf': False, 'risk_level': 'low'},
        'legal_basis': [{'norm_number': '8.212', 'norm_year': 1991, 'article': 'Art. 28, par. 9, d', 'is_primary': True,
            'excerpt': 'Nao integram o salario de contribuicao as importancias recebidas a titulo de ferias indenizadas e respectivo adicional constitucional.'}],
    },

    # ── 13 Salario completo ───────────────────────────────────────────────────
    {
        'name': '13 Salario Rescisorio',
        'code': '13SR01',
        'description': 'Gratificacao natalina proporcional paga na rescisao: 1/12 avos por mes trabalhado no ano.',
        'category': 'Proventos',
        'esocial_nature_code': '1310',
        'incidence': {'inss': True, 'fgts': True, 'irrf': True, 'risk_level': 'low',
                      'inss_observation': 'O 13 rescisorio e calculado separadamente do salario mensal da rescisao.'},
        'legal_basis': [{'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943, 'article': 'Art. 7, VIII CF/88', 'is_primary': True,
            'excerpt': 'Na rescisao, o empregado tem direito a proporcao de 1/12 avos do 13 salario por mes trabalhado ou fracao igual ou superior a 15 dias.'}],
    },
    {
        'name': 'INSS sobre 13 Salario (Desconto)',
        'code': 'INS13S',
        'description': 'Desconto da contribuicao previdenciaria calculada separadamente sobre a 2a parcela do 13 salario.',
        'category': 'Descontos',
        'esocial_nature_code': '9120',
        'incidence': {'inss': False, 'fgts': False, 'irrf': False, 'risk_level': 'low'},
        'legal_basis': [{'norm_number': '8.212', 'norm_year': 1991, 'article': 'Art. 28, par. 7', 'is_primary': True,
            'excerpt': 'O decimo terceiro salario integra o salario de contribuicao, excetuada a parcela paga como primeiro adiantamento.'}],
    },
    {
        'name': 'IRRF sobre 13 Salario (Desconto)',
        'code': 'IRR13S',
        'description': 'IRRF retido sobre a 2a parcela do 13 salario, com calculo exclusivo e separado do salario mensal.',
        'category': 'Descontos',
        'esocial_nature_code': '9130',
        'incidence': {'inss': False, 'fgts': False, 'irrf': False, 'risk_level': 'medium',
                      'irrf_observation': 'O IRRF do 13 salario tem calculo exclusivo — nao acumula com outros rendimentos mensais do mesmo periodo.'},
        'legal_basis': [{'norm_number': '9.250', 'norm_year': 1995, 'article': 'Art. 16', 'is_primary': True,
            'excerpt': 'O imposto sobre a renda incidente sobre a gratificacao de Natal (13 salario) sera calculado exclusivamente sobre esse valor, nao se acumulando com os demais rendimentos mensais.'}],
    },
    {
        'name': 'Adiantamento de 13 (Desconto 2a Parcela)',
        'code': 'ADT13S',
        'description': 'Desconto do valor adiantado na 1a parcela no momento do pagamento da 2a parcela do 13 salario.',
        'category': 'Descontos',
        'esocial_nature_code': '9200',
        'incidence': {'inss': False, 'fgts': False, 'irrf': False, 'risk_level': 'low'},
        'legal_basis': [{'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943, 'article': 'Art. 7, VIII CF/88', 'is_primary': True,
            'excerpt': 'O adiantamento da 1a parcela do 13 salario e compensado integralmente no pagamento da 2a parcela em dezembro.'}],
    },

    # ── Verbas rescisorias avancadas ──────────────────────────────────────────
    {
        'name': 'Aviso Previo Proporcional',
        'code': 'APP001',
        'description': 'Acrescimo de 3 dias por ano de servico ao aviso previo, ate 60 dias adicionais (maximo 90 dias total).',
        'category': 'Proventos',
        'esocial_nature_code': '1305',
        'incidence': {'inss': False, 'fgts': True, 'irrf': False, 'risk_level': 'medium',
                      'fgts_observation': 'Os dias proporcionais integram a base de calculo do FGTS rescisorio.',
                      'irrf_observation': 'Natureza indenizatoria — isento de IRRF.'},
        'legal_basis': [{'norm_number': '12.506', 'norm_year': 2011, 'article': 'Art. 1', 'is_primary': True,
            'excerpt': 'O aviso previo sera concedido na proporcao de 30 dias ao empregado que contar ate 1 ano de servico, com acrescimo de 3 dias por ano de servico, ate o maximo de 60 dias.'}],
    },
    {
        'name': 'Multa FGTS 20% — Rescisao Consensual',
        'code': 'MUL020',
        'description': 'Multa de 20% sobre o saldo do FGTS devida na rescisao por acordo (distrato) entre empregado e empregador.',
        'category': 'Proventos',
        'esocial_nature_code': '9910',
        'incidence': {'inss': False, 'fgts': False, 'irrf': False, 'risk_level': 'medium'},
        'legal_basis': [{'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943, 'article': 'Art. 484-A', 'is_primary': True,
            'excerpt': 'O contrato de trabalho podera ser extinto por acordo entre empregado e empregador. Nesse caso, sera devida multa de 20% sobre o saldo do FGTS.'}],
    },
    {
        'name': 'FGTS Rescisorio (Informativo)',
        'code': 'FGR001',
        'description': 'Saldo total do FGTS liberado ao empregado dispensado sem justa causa.',
        'category': 'Informativos',
        'esocial_nature_code': '9920',
        'incidence': {'inss': False, 'fgts': False, 'irrf': False, 'risk_level': 'low'},
        'legal_basis': [{'norm_number': '8.036', 'norm_year': 1990, 'article': 'Art. 18', 'is_primary': True,
            'excerpt': 'Ocorrendo rescisao do contrato de trabalho sem justa causa, o trabalhador podera movimentar a totalidade dos depositos da conta vinculada do FGTS.'}],
    },
    {
        'name': 'Rescisao Indireta — Verbas Devidas',
        'code': 'RIN001',
        'description': 'Verbas pagas ao empregado que rescinde o contrato por falta grave do empregador (rescisao indireta).',
        'category': 'Informativos',
        'esocial_nature_code': '1351',
        'incidence': {'inss': False, 'fgts': True, 'irrf': False, 'risk_level': 'high',
                      'fgts_observation': 'Na rescisao indireta o empregado recebe as mesmas verbas da dispensa sem justa causa, incluindo multa de 40% do FGTS.',
                      'irrf_observation': 'Verbas indenizatorias da rescisao sao isentas de IRRF.'},
        'legal_basis': [{'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943, 'article': 'Art. 483', 'is_primary': True,
            'excerpt': 'O empregado podera considerar rescindido o contrato e pleitear a devida indenizacao quando o empregador descumprir obrigacoes contratuais ou praticar ato ilicito.'}],
    },
    {
        'name': 'Indenizacao — Dispensa Discriminatoria',
        'code': 'IDD001',
        'description': 'Indenizacao adicional devida ao empregado dispensado por ato discriminatorio (doenca, raca, genero etc.).',
        'category': 'Informativos',
        'esocial_nature_code': '1351',
        'incidence': {'inss': False, 'fgts': False, 'irrf': False, 'risk_level': 'high',
                      'inss_observation': 'Verba indenizatoria — nao incide qualquer encargo trabalhista ou tributario.'},
        'legal_basis': [{'norm_number': '9.029', 'norm_year': 1995, 'article': 'Art. 4', 'is_primary': True,
            'excerpt': 'O rompimento da relacao de trabalho por ato discriminatorio faculta ao empregado optar entre a reintegracao com ressarcimento integral ou a percepcao, em dobro, da remuneracao do periodo de afastamento.'}],
    },

    # ── Descontos do empregado ─────────────────────────────────────────────────
    {
        'name': 'Desconto por Faltas e Atrasos',
        'code': 'FAL001',
        'description': 'Desconto proporcional ao salario pelas ausencias e atrasos injustificados no periodo.',
        'category': 'Descontos',
        'esocial_nature_code': '9150',
        'incidence': {'inss': False, 'fgts': False, 'irrf': False, 'risk_level': 'low'},
        'legal_basis': [{'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943, 'article': 'Art. 462', 'is_primary': True,
            'excerpt': 'Ao empregador e vedado efetuar qualquer desconto nos salarios do empregado, salvo quando resultar de adiantamentos, dispositivos de lei ou contrato coletivo.'}],
    },
    {
        'name': 'DSR sobre Faltas',
        'code': 'DSF001',
        'description': 'Desconto do Descanso Semanal Remunerado correspondente as semanas com falta injustificada.',
        'category': 'Descontos',
        'esocial_nature_code': '9160',
        'incidence': {'inss': False, 'fgts': False, 'irrf': False, 'risk_level': 'low'},
        'legal_basis': [{'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943, 'article': 'Art. 473 c/c Lei 605/1949, Art. 3', 'is_primary': True,
            'excerpt': 'O empregado que faltar injustificadamente perde o direito a remuneracao do descanso semanal da semana correspondente a falta.'}],
    },
    {
        'name': 'Emprestimo Consignado (Desconto)',
        'code': 'CON001',
        'description': 'Desconto de parcelas de credito consignado autorizado pelo empregado, direto na folha de pagamento.',
        'category': 'Descontos',
        'esocial_nature_code': '9170',
        'incidence': {'inss': False, 'fgts': False, 'irrf': False, 'risk_level': 'low'},
        'legal_basis': [{'norm_number': '14.601', 'norm_year': 2023, 'article': 'Art. 1', 'is_primary': True,
            'excerpt': 'E permitida a consignacao em folha de pagamento de operacoes de credito contratadas pelo empregado com instituicao financeira autorizada pelo empregador.'}],
    },
    {
        'name': 'Contribuicao Sindical (Facultativa)',
        'code': 'CSF001',
        'description': 'Desconto da contribuicao sindical anual, somente com autorizacao previa e expressa do empregado.',
        'category': 'Descontos',
        'esocial_nature_code': '9180',
        'incidence': {'inss': False, 'fgts': False, 'irrf': False, 'risk_level': 'medium',
                      'inss_observation': 'Apos Reforma Trabalhista (Lei 13.467/2017), a contribuicao sindical so pode ser descontada com autorizacao expressa e individual do empregado.'},
        'legal_basis': [{'norm_number': '13.467', 'norm_year': 2017, 'article': 'Art. 545 CLT', 'is_primary': True,
            'excerpt': 'Os empregadores ficam obrigados a descontar da folha de pagamento dos seus empregados, desde que por eles devidamente autorizados, as contribuicoes devidas ao sindicato.'}],
    },

    # ── Beneficios avancados ───────────────────────────────────────────────────
    {
        'name': 'Auxilio Educacao / Bolsa de Estudos',
        'code': 'EDU001',
        'description': 'Custeio de curso, graduacao ou pos-graduacao pela empresa; isento quando vinculado a atividade empresarial.',
        'category': 'Informativos',
        'esocial_nature_code': '5020',
        'incidence': {'inss': False, 'fgts': False, 'irrf': False, 'risk_level': 'medium',
                      'inss_observation': 'Nao incide quando o beneficio e vinculado a atividade da empresa e disponivel a todos os empregados. Caso contrario, pode ser salario in natura.'},
        'legal_basis': [{'norm_number': '8.212', 'norm_year': 1991, 'article': 'Art. 28, par. 9, t', 'is_primary': True,
            'excerpt': 'Nao integram o salario de contribuicao os valores relativos a assistencia prestada por servico medico ou odontologico, inclusive o reembolso de despesas com medicamentos e bolsas de estudo.'}],
    },
    {
        'name': 'Vale-Combustivel / Auxilio Combustivel',
        'code': 'VCO001',
        'description': 'Auxilio em combustivel pago ao empregado que usa veiculo proprio a servico da empresa.',
        'category': 'Informativos',
        'esocial_nature_code': '5030',
        'incidence': {'inss': False, 'fgts': False, 'irrf': False, 'risk_level': 'medium',
                      'inss_observation': 'Nao incide quando configurado como ressarcimento de despesas comprovadas, sem habitualidade salarial. Pagamento habitual sem comprovacao pode ser enquadrado como salario in natura.'},
        'legal_basis': [{'norm_number': '8.212', 'norm_year': 1991, 'article': 'Art. 28, par. 9, f', 'is_primary': True,
            'excerpt': 'Nao integram o salario de contribuicao o ressarcimento de despesas pelo uso de veiculo do empregado.'}],
    },
    {
        'name': 'Auxilio Farmacia',
        'code': 'AFR001',
        'description': 'Reembolso de despesas com medicamentos fornecido pela empresa como beneficio assistencial.',
        'category': 'Informativos',
        'esocial_nature_code': '5060',
        'incidence': {'inss': False, 'fgts': False, 'irrf': False, 'risk_level': 'low'},
        'legal_basis': [{'norm_number': '8.212', 'norm_year': 1991, 'article': 'Art. 28, par. 9', 'is_primary': True,
            'excerpt': 'Beneficios assistenciais concedidos pela empresa sem carater salarial nao integram o salario de contribuicao previdenciaria.'}],
    },
    {
        'name': 'Auxilio Moradia',
        'code': 'AMO001',
        'description': 'Auxilio pago pela empresa para custeio parcial ou integral da moradia do empregado.',
        'category': 'Proventos',
        'esocial_nature_code': '5070',
        'incidence': {'inss': True, 'fgts': True, 'irrf': True, 'risk_level': 'high',
                      'inss_observation': 'Integra o salario de contribuicao quando pago habitualmente, salvo se configurado como cessao de habitacao em local de dificil acesso (Art. 458, CLT).'},
        'legal_basis': [{'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943, 'article': 'Art. 458', 'is_primary': True,
            'excerpt': 'Alem do pagamento em dinheiro, compreende-se no salario a habitacao prestada in natura que a empresa, por forca do contrato ou do costume, fornecer habitualmente ao empregado.'}],
    },
    {
        'name': 'Previdencia Complementar (Cota Empregador)',
        'code': 'PVC001',
        'description': 'Contribuicao da empresa a plano de previdencia complementar aberto ou fechado em favor do empregado.',
        'category': 'Informativos',
        'esocial_nature_code': '5040',
        'incidence': {'inss': False, 'fgts': False, 'irrf': False, 'risk_level': 'low'},
        'legal_basis': [{'norm_number': '8.212', 'norm_year': 1991, 'article': 'Art. 28, par. 9, p', 'is_primary': True,
            'excerpt': 'Nao integram o salario de contribuicao o valor das contribuicoes efetivamente pago pela pessoa juridica relativo a programa de previdencia complementar, aberto ou fechado.'}],
    },

    # ── Bases de calculo e informativos ───────────────────────────────────────
    {
        'name': 'Base de Calculo INSS (Informativo)',
        'code': 'BINSS1',
        'description': 'Soma de todas as verbas salariais que compoem a base de calculo das contribuicoes previdenciarias.',
        'category': 'Bases de C\u00e1lculo',
        'esocial_nature_code': '9001',
        'incidence': {'inss': False, 'fgts': False, 'irrf': False, 'risk_level': 'low'},
        'legal_basis': [{'norm_number': '8.212', 'norm_year': 1991, 'article': 'Art. 28', 'is_primary': True,
            'excerpt': 'Entende-se por salario de contribuicao a totalidade dos rendimentos pagos, devidos ou creditados a qualquer titulo, durante o mes, destinados a retribuir o trabalho.'}],
    },
    {
        'name': 'Base de Calculo IRRF (Informativo)',
        'code': 'BIRRF1',
        'description': 'Rendimentos tributaveis menos deducoes legais (INSS, dependentes, pensao alimenticia).',
        'category': 'Bases de C\u00e1lculo',
        'esocial_nature_code': '9003',
        'incidence': {'inss': False, 'fgts': False, 'irrf': False, 'risk_level': 'low'},
        'legal_basis': [{'norm_number': '9.250', 'norm_year': 1995, 'article': 'Art. 4', 'is_primary': True,
            'excerpt': 'A base de calculo do IRRF mensal e composta pelos rendimentos tributaveis, deduzidas as contribuicoes previdenciarias, as parcelas por dependentes e pensao alimenticia.'}],
    },
    {
        'name': 'Base de Calculo FGTS (Informativo)',
        'code': 'BFGTS1',
        'description': 'Remuneracao mensal total que serve de base para o deposito do FGTS pelo empregador.',
        'category': 'Bases de C\u00e1lculo',
        'esocial_nature_code': '9100',
        'incidence': {'inss': False, 'fgts': False, 'irrf': False, 'risk_level': 'low'},
        'legal_basis': [{'norm_number': '8.036', 'norm_year': 1990, 'article': 'Art. 15', 'is_primary': True,
            'excerpt': 'Os empregadores ficam obrigados a depositar 8% da remuneracao do empregado na conta vinculada do FGTS, ate o dia 7 de cada mes.'}],
    },
    {
        'name': 'FGTS Mensal (Deposito Empresa)',
        'code': 'FGM001',
        'description': 'Deposito mensal de 8% sobre a remuneracao, realizado pela empresa na conta vinculada do empregado.',
        'category': 'Informativos',
        'esocial_nature_code': '9100',
        'incidence': {'inss': False, 'fgts': False, 'irrf': False, 'risk_level': 'low'},
        'legal_basis': [{'norm_number': '8.036', 'norm_year': 1990, 'article': 'Art. 15, caput', 'is_primary': True,
            'excerpt': 'Os empregadores ficam obrigados a depositar, ate o dia 7 de cada mes, em conta bancaria vinculada, a importancia correspondente a 8% da remuneracao paga ou devida no mes anterior a cada trabalhador.'}],
    },

    # ── Licencas e afastamentos ────────────────────────────────────────────────
    {
        'name': 'Salario-Maternidade',
        'code': 'MAT001',
        'description': 'Beneficio pago pelo INSS durante a licenca-maternidade de 120 ou 180 dias (Empresa Cidada).',
        'category': 'Proventos',
        'esocial_nature_code': '1400',
        'incidence': {'inss': False, 'fgts': True, 'irrf': True, 'risk_level': 'medium',
                      'inss_observation': 'O salario-maternidade nao integra o salario de contribuicao do segurado. A empresa antecipa o beneficio e deduz da guia GPS.',
                      'fgts_observation': 'O FGTS continua sendo depositado pela empresa durante toda a licenca-maternidade.',
                      'irrf_observation': 'O salario-maternidade e tributavel pelo IRRF, conforme tabela progressiva.'},
        'legal_basis': [{'norm_number': '8.213', 'norm_year': 1991, 'article': 'Art. 72', 'is_primary': True,
            'excerpt': 'O salario-maternidade para a segurada empregada consiste numa renda mensal igual a sua remuneracao integral durante 120 dias.'}],
    },
    {
        'name': 'Licenca Paternidade',
        'code': 'PAT001',
        'description': 'Licenca de 5 dias (ou 20 dias para Empresa Cidada) por nascimento, adocao ou guarda judicial do filho.',
        'category': 'Proventos',
        'esocial_nature_code': '1410',
        'incidence': {'inss': True, 'fgts': True, 'irrf': True, 'risk_level': 'low'},
        'legal_basis': [{'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943, 'article': 'Art. 473, III', 'is_primary': True,
            'excerpt': 'O empregado podera deixar de comparecer ao servico por 5 dias consecutivos em caso de nascimento de filho, no decorrer da primeira semana.'}],
    },
    {
        'name': 'Auxilio-Doenca Previdenciario (INSS)',
        'code': 'ADP001',
        'description': 'Beneficio pago pelo INSS a partir do 16 dia de afastamento por doenca nao ocupacional.',
        'category': 'Informativos',
        'esocial_nature_code': '1420',
        'incidence': {'inss': False, 'fgts': False, 'irrf': False, 'risk_level': 'low',
                      'inss_observation': 'O beneficio e pago pelo INSS. A empresa paga os primeiros 15 dias (com incidencia normal de encargos); do 16 dia em diante, e o INSS que paga.',
                      'fgts_observation': 'O FGTS NAO e depositado durante o auxilio-doenca previdenciario (salvo norma coletiva em contrario).'},
        'legal_basis': [{'norm_number': '8.213', 'norm_year': 1991, 'article': 'Art. 75', 'is_primary': True,
            'excerpt': 'O auxilio-doenca sera devido ao segurado que ficar incapacitado para o seu trabalho por mais de 15 dias consecutivos.'}],
    },
    {
        'name': 'Auxilio-Doenca Acidentario (CAT)',
        'code': 'ADA001',
        'description': 'Beneficio pago pelo INSS em decorrencia de acidente de trabalho; FGTS depositado pela empresa durante todo afastamento.',
        'category': 'Informativos',
        'esocial_nature_code': '1430',
        'incidence': {'inss': False, 'fgts': True, 'irrf': False, 'risk_level': 'high',
                      'fgts_observation': 'A empresa DEVE continuar depositando o FGTS durante o afastamento acidentario (Art. 15, par. 5, Lei 8.036). Diferentemente do auxilio-doenca comum.',
                      'inss_observation': 'O beneficio e pago pelo INSS. A empresa deposita o FGTS e mantem o plano de saude.'},
        'legal_basis': [{'norm_number': '8.213', 'norm_year': 1991, 'article': 'Art. 86', 'is_primary': True,
            'excerpt': 'O auxilio-acidente sera concedido ao segurado quando, apos consolidacao das lesoes decorrentes de acidente de qualquer natureza, resultarem sequelas que impliquem reducao da capacidade para o trabalho.'}],
    },
    {
        'name': 'Primeiros 15 Dias de Afastamento (Doenca)',
        'code': 'AF15D1',
        'description': 'Salario pago pelo empregador nos primeiros 15 dias de afastamento por doenca, antes da concessao do auxilio-doenca.',
        'category': 'Proventos',
        'esocial_nature_code': '1010',
        'incidence': {'inss': True, 'fgts': True, 'irrf': True, 'risk_level': 'low',
                      'inss_observation': 'Nos primeiros 15 dias de afastamento, o empregado ainda recebe da empresa, com incidencia normal de INSS e FGTS.'},
        'legal_basis': [{'norm_number': '8.213', 'norm_year': 1991, 'article': 'Art. 60, par. 3', 'is_primary': True,
            'excerpt': 'Durante os primeiros quinze dias consecutivos ao afastamento da atividade por doenca, incumbira a empresa pagar ao segurado empregado o seu salario integral.'}],
    },

    # ── Regimes especiais ──────────────────────────────────────────────────────
    {
        'name': 'Aprendiz — Salario',
        'code': 'APR001',
        'description': 'Remuneracao do empregado aprendiz (14 a 24 anos) com FGTS reduzido a 2%.',
        'category': 'Proventos',
        'esocial_nature_code': '1600',
        'incidence': {'inss': True, 'fgts': True, 'irrf': True, 'risk_level': 'medium',
                      'fgts_observation': 'A aliquota do FGTS para aprendiz e de 2% (reduzida), conforme Art. 15, par. 7, Lei 8.036/1990.',
                      'inss_observation': 'O INSS e calculado normalmente pela tabela vigente.'},
        'legal_basis': [{'norm_number': '10.097', 'norm_year': 2000, 'article': 'Art. 428, CLT', 'is_primary': True,
            'excerpt': 'Considera-se aprendiz o maior de quatorze e menor de vinte e quatro anos que celebre contrato de aprendizagem com empresa, com formacao tecnico-profissional metodica.'}],
    },
    {
        'name': 'Estagiario — Bolsa Auxilio',
        'code': 'EST001',
        'description': 'Bolsa auxilio paga ao estagiario em estagio nao obrigatorio; nao cria vinculo empregaticio.',
        'category': 'Informativos',
        'esocial_nature_code': '1610',
        'incidence': {'inss': False, 'fgts': False, 'irrf': False, 'risk_level': 'low',
                      'inss_observation': 'O estagio nao gera vinculo empregaticio (Lei 11.788/2008). Nao incide INSS, FGTS ou encargos trabalhistas.',
                      'irrf_observation': 'A bolsa e isenta de IRRF dentro dos limites da tabela progressiva.'},
        'legal_basis': [{'norm_number': '11.788', 'norm_year': 2008, 'article': 'Art. 12', 'is_primary': True,
            'excerpt': 'O estagio, como ato educativo escolar supervisionado, nao cria vinculo empregaticio de qualquer natureza.'}],
    },
    {
        'name': 'Domestico — Salario Base',
        'code': 'DOM001',
        'description': 'Remuneracao base do empregado domestico, regido pela LC 150/2015 (PEC do Domestico).',
        'category': 'Proventos',
        'esocial_nature_code': '1620',
        'incidence': {'inss': True, 'fgts': True, 'irrf': True, 'risk_level': 'medium',
                      'fgts_observation': 'A aliquota do FGTS domestico e 8% (empregado) + 3,2% (empregador, para constituicao de fundo de rescisao futura). Recolhimento pelo DAE.',
                      'inss_observation': 'O INSS do domestico segue a tabela padrao. O empregador domestico recolhe 8% de contribuicao patronal + 0,8% RAT.'},
        'legal_basis': [{'norm_number': '150', 'norm_year': 2015, 'article': 'Art. 1', 'is_primary': True,
            'excerpt': 'Ao empregado domestico aplica-se o disposto nesta Lei Complementar, que dispoe sobre a relacao de trabalho domestico.'}],
    },
    {
        'name': 'Autonomo — Remuneracao (RPA)',
        'code': 'RPA001',
        'description': 'Pagamento a trabalhador autonomo mediante Recibo de Pagamento a Autonomo, com retencao de INSS e IRRF.',
        'category': 'Informativos',
        'esocial_nature_code': '1000',
        'incidence': {'inss': True, 'fgts': False, 'irrf': True, 'risk_level': 'high',
                      'inss_observation': 'A empresa retém 11% de INSS do autonomo (contribuicao do segurado) e recolhe mais 20% como contribuicao patronal.',
                      'fgts_observation': 'Nao ha FGTS para autonomos — ausencia de vinculo empregaticio.',
                      'irrf_observation': 'Incide IRRF conforme tabela progressiva, sobre o valor bruto da RPA deduzido o INSS retido.'},
        'legal_basis': [{'norm_number': '8.212', 'norm_year': 1991, 'article': 'Art. 22, III', 'is_primary': True,
            'excerpt': 'A contribuicao a cargo da empresa destinada a Seguridade Social e de 20% sobre o total das remuneracoes pagas, devidas ou creditadas a qualquer titulo aos segurados contribuintes individuais.'}],
    },

    # ── Situacoes especiais ────────────────────────────────────────────────────
    {
        'name': 'PPR — Programa de Participacao em Resultados',
        'code': 'PPR001',
        'description': 'Participacao em resultados baseada em metas qualitativas ou quantitativas, formalizada em acordo coletivo.',
        'category': 'Proventos',
        'esocial_nature_code': '1200',
        'incidence': {'inss': False, 'fgts': False, 'irrf': True, 'risk_level': 'medium',
                      'inss_observation': 'Nao incide INSS/FGTS quando devidamente formalizada em acordo coletivo, com periodicidade minima semestral.',
                      'irrf_observation': 'Incide IRRF com tabela exclusiva de PLR/PPR, nao acumulando com o salario do mes.'},
        'legal_basis': [{'norm_number': '10.101', 'norm_year': 2000, 'article': 'Art. 3', 'is_primary': True,
            'excerpt': 'A participacao nos lucros ou resultados nao substitui nem complementa a remuneracao, nem constitui base de incidencia de qualquer encargo trabalhista.'}],
    },
    {
        'name': 'Reembolso de Despesas (Geral)',
        'code': 'REM001',
        'description': 'Ressarcimento de despesas realizadas pelo empregado a servico da empresa, mediante comprovacao.',
        'category': 'Informativos',
        'esocial_nature_code': '1210',
        'incidence': {'inss': False, 'fgts': False, 'irrf': False, 'risk_level': 'low',
                      'inss_observation': 'Nao incide quando ha comprovacao da despesa (nota fiscal) e o reembolso e pelo valor exato. Sem comprovacao pode ser enquadrado como rendimento tributavel.'},
        'legal_basis': [{'norm_number': '8.212', 'norm_year': 1991, 'article': 'Art. 28, par. 9', 'is_primary': True,
            'excerpt': 'Nao integram o salario de contribuicao os valores correspondentes a ressarcimento de despesas do empregado quando devidamente comprovadas.'}],
    },
    {
        'name': 'Estabilidade Provisoria — Salario Indenizatorio',
        'code': 'EST002',
        'description': 'Salarios devidos ao empregado com estabilidade indevidamente dispensado, correspondentes ao periodo de vedacao.',
        'category': 'Informativos',
        'esocial_nature_code': '1350',
        'incidence': {'inss': True, 'fgts': True, 'irrf': True, 'risk_level': 'high',
                      'inss_observation': 'Os salarios do periodo de estabilidade tem natureza remuneratoria e integram o salario de contribuicao.',
                      'irrf_observation': 'Sao tributaveis pelo IRRF, pois correspondem a salarios devidos.'},
        'legal_basis': [{'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943, 'article': 'Art. 10, II, ADCT', 'is_primary': True,
            'excerpt': 'Sao vedadas dispensa arbitraria ou sem justa causa do empregado eleito para cargos de direcao de CIPA desde o registro de sua candidatura ate um ano apos o final de seu mandato.'}],
    },
]


class Command(BaseCommand):
    help = 'Seed v1.1 — adiciona 55 rubricas (jornada, rescisórias, doméstico, licenças, bases)'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        from apps.catalog.models import Category, EsocialNature, Rubric
        from apps.legislation.models import LegalNorm, LegalBasis
        from apps.engine.models import Incidence

        self.stdout.write('Criando naturezas eSocial v1.1...')
        for data in V11_NATURES:
            EsocialNature.objects.get_or_create(
                code=data['code'],
                defaults={
                    'description': data['description'],
                    'is_salary_nature': data['is_salary_nature'],
                }
            )

        self.stdout.write('Criando normas legais v1.1...')
        norm_map = {}
        for norm in LegalNorm.objects.all():
            norm_map[(norm.number, norm.year)] = norm

        for data in V11_NORMS:
            norm, _ = LegalNorm.objects.get_or_create(
                number=data['number'],
                year=data['year'],
                defaults=data
            )
            norm_map[(data['number'], data['year'])] = norm

        self.stdout.write('Criando rubricas v1.1...')
        created_count = 0
        for r in RUBRICAS_V11:
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
            else:
                self.stdout.write(f'  = {rubric.name} (ja existe)')

        self.stdout.write(self.style.SUCCESS(
            f'\n{created_count} rubricas adicionadas.'
            f' Total no banco: {Rubric.objects.count()} rubricas'
            f' / {Incidence.objects.count()} incidencias.'
        ))
