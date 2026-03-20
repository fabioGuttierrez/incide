"""
Seed v1.2 — 20 rubricas cobrindo lacunas identificadas:
  - Quebra de caixa, anuênio, acúmulo de função
  - Hora extra por interjornada insuficiente
  - Salário in natura (habitação e alimentação não PAT)
  - Licenças remuneradas (gala, nojo, art. 473)
  - Primeiros 15 dias — acidente de trabalho
  - Multas rescisórias (arts. 467 e 477)
  - Indenizações de estabilidade (gestante, CIPA)
  - Pró-labore, Stock Options, Previdência Complementar (desconto)
  - Complemento salarial s/ auxílio-doença, Dobra de férias
  - RAT/FAP — base informativa

Execute com: python manage.py seed_v12_rubricas
"""
from django.core.management.base import BaseCommand
from django.db import transaction


V12_NATURES = [
    {'code': '1220', 'description': 'Quebra de Caixa / Complemento Funcional', 'is_salary_nature': False},
    {'code': '1230', 'description': 'Adicional de Acumulo de Funcao', 'is_salary_nature': True},
    {'code': '1240', 'description': 'Adicional por Tempo de Servico / Anuenio', 'is_salary_nature': True},
    {'code': '1360', 'description': 'Multa Rescisoria (Arts. 467 e 477 CLT)', 'is_salary_nature': False},
    {'code': '5010', 'description': 'Alimentacao Fornecida — Nao PAT (Natureza Salarial)', 'is_salary_nature': True},
    {'code': '5080', 'description': 'Habitacao Fornecida (Natureza Salarial)', 'is_salary_nature': True},
    {'code': '9190', 'description': 'Previdencia Complementar (Desconto Empregado)', 'is_salary_nature': False},
    {'code': '9300', 'description': 'Pro-Labore — Socio-Administrador', 'is_salary_nature': False},
    {'code': '1260', 'description': 'Stock Options — Exercicio de Opcao de Compra', 'is_salary_nature': False},
]

V12_NORMS = [
    {
        'norm_type': 'lc', 'number': '116', 'year': 2003,
        'title': 'LC 116/2003 — Imposto Sobre Servicos de Qualquer Natureza',
        'official_link': 'https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp116.htm',
    },
    {
        'norm_type': 'in', 'number': '2.180', 'year': 2024,
        'title': 'IN RFB 2.180/2024 — Tributacao de Stock Options',
        'official_link': 'https://www.in.gov.br/en/web/dou/-/instrucao-normativa-rfb-n-2-180-de-11-de-marco-de-2024',
    },
    {
        'norm_type': 'lei', 'number': '6.404', 'year': 1976,
        'title': 'Lei 6.404/1976 — Sociedades por Acoes (Stock Options)',
        'official_link': 'https://www.planalto.gov.br/ccivil_03/leis/l6404consol.htm',
    },
    {
        'norm_type': 'lei', 'number': '9.532', 'year': 1997,
        'title': 'Lei 9.532/1997 — Previdencia Complementar e IRRF',
        'official_link': 'https://www.planalto.gov.br/ccivil_03/leis/l9532.htm',
    },
]

RUBRICAS_V12 = [

    # ── Adicionais especiais ───────────────────────────────────────────────────
    {
        'name': 'Quebra de Caixa',
        'code': 'QCX001',
        'description': 'Adicional pago a empregados que manuseiam dinheiro, para compensar possíveis diferenças de caixa. Natureza jurídica controversa: TST tende a considerar indenizatório se pago em valor fixo razoável.',
        'category': 'Proventos',
        'esocial_nature_code': '1220',
        'incidence': {
            'inss': False, 'fgts': False, 'irrf': True, 'risk_level': 'medium',
            'inss_observation': 'TST (OJ 247 SDI-I) entende que quebra de caixa é indenizatório, desde que pago em valor fixo e razoável. Pagamento excessivo ou habitual pode ser recaracterizado como salário.',
            'irrf_observation': 'Incide IRRF por ser rendimento do trabalho, mesmo com natureza indenizatória para fins trabalhistas.',
            'risk_reason': 'Divergência entre TST (indenizatório) e RFB (tributável pelo IRRF). Pagamentos em valor elevado ou variável aumentam o risco de recaracterização como salário, atraindo INSS e FGTS.',
        },
        'legal_basis': [{'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943, 'article': 'OJ 247 SDI-I TST', 'is_primary': True,
            'excerpt': 'A parcela paga aos bancários sob a denominação quebra de caixa possui natureza indenizatória e, por isso, não integra o salário do prestador de serviços.'}],
    },
    {
        'name': 'Adicional por Tempo de Serviço (Anuênio)',
        'code': 'ATS001',
        'description': 'Percentual adicional ao salário por cada ano de serviço prestado ao mesmo empregador, previsto em norma coletiva ou regulamento interno.',
        'category': 'Proventos',
        'esocial_nature_code': '1240',
        'incidence': {
            'inss': True, 'fgts': True, 'irrf': True, 'risk_level': 'low',
            'risk_reason': 'Rubrica de baixo risco: possui natureza salarial pacífica e integra habitualmente a remuneração para todos os encargos.',
        },
        'legal_basis': [{'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943, 'article': 'Art. 457, caput', 'is_primary': True,
            'excerpt': 'Compreendem-se na remuneração do empregado, para todos os efeitos legais, além do salário devido e pago diretamente pelo empregador, como contraprestação do serviço, as gorjetas que receber.'}],
    },
    {
        'name': 'Adicional de Acúmulo de Função',
        'code': 'ACF001',
        'description': 'Valor pago ao empregado que exerce permanentemente atribuições além do seu cargo original, mediante acordo ou norma coletiva.',
        'category': 'Proventos',
        'esocial_nature_code': '1230',
        'incidence': {
            'inss': True, 'fgts': True, 'irrf': True, 'risk_level': 'medium',
            'inss_observation': 'Integra o salário de contribuição por ser verba habitual de natureza salarial.',
            'risk_reason': 'Risco médio: o direito ao adicional depende de convenção coletiva ou acordo individual escrito. Sem previsão normativa clara, o empregado pode reclamar a diferença retroativa, gerando passivo.',
        },
        'legal_basis': [{'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943, 'article': 'Sumula 159 TST', 'is_primary': True,
            'excerpt': 'Enquanto perdurar a substituição que não tenha caráter meramente eventual, inclusive nas férias, o empregado substituto fará jus ao salário contratual do substituído.'}],
    },
    {
        'name': 'Hora Extra por Interjornada Insuficiente',
        'code': 'HEI001',
        'description': 'Pagamento do período de descanso interjornada (mínimo 11 horas) não concedido, calculado como horas extras.',
        'category': 'Proventos',
        'esocial_nature_code': '1040',
        'incidence': {
            'inss': True, 'fgts': True, 'irrf': True, 'risk_level': 'medium',
            'inss_observation': 'Integra a base de contribuição como hora extra de natureza salarial.',
            'risk_reason': 'Risco médio: a jurisprudência do TST (Súmula 110) é pacífica, mas o cálculo (horas ou período suprimido) é frequentemente disputado. Empregadores que não controlam a interjornada ficam expostos a autuações fiscais.',
        },
        'legal_basis': [{'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943, 'article': 'Art. 66 c/c Sumula 110 TST', 'is_primary': True,
            'excerpt': 'No regime de revezamento, as horas trabalhadas em seguida ao repouso semanal do empregado, com prejuízo do intervalo mínimo de onze horas consecutivas para descanso entre jornadas, devem ser remuneradas como extraordinárias.'}],
    },

    # ── Salário in natura ──────────────────────────────────────────────────────
    {
        'name': 'Salário in Natura — Habitação Fornecida',
        'code': 'SIN001',
        'description': 'Imóvel cedido pelo empregador como parte da remuneração (residência funcional). Tem natureza salarial salvo quando indispensável ao trabalho.',
        'category': 'Proventos',
        'esocial_nature_code': '5080',
        'incidence': {
            'inss': True, 'fgts': True, 'irrf': True, 'risk_level': 'high',
            'inss_observation': 'Integra o salário de contribuição pelo valor real ou pelo percentual de 20% do valor do salário do empregado (§ 3º do art. 458 CLT).',
            'irrf_observation': 'Deve ser incluído na base de cálculo do IRRF mensalmente pelo valor de mercado da cessão.',
            'risk_reason': 'Alto risco: a distinção entre habitação cedida como salário (tributável) e aquela indispensável ao trabalho (indenizatória) é subjetiva e frequentemente contestada em fiscalização. A falta de comprovação da necessidade operacional impõe todos os encargos.',
        },
        'legal_basis': [{'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943, 'article': 'Art. 458, par. 2, II', 'is_primary': True,
            'excerpt': 'Não serão considerados como salário, para os efeitos desta Consolidação, os vestuários, equipamentos e outros acessórios fornecidos ao empregado e utilizados no local de trabalho, para a prestação do serviço.'}],
    },
    {
        'name': 'Salário in Natura — Alimentação (Não PAT)',
        'code': 'SIA001',
        'description': 'Alimentação fornecida fora do Programa de Alimentação do Trabalhador (PAT); possui natureza salarial e integra todos os encargos.',
        'category': 'Proventos',
        'esocial_nature_code': '5010',
        'incidence': {
            'inss': True, 'fgts': True, 'irrf': True, 'risk_level': 'high',
            'inss_observation': 'Alimentação fornecida fora do PAT integra o salário de contribuição. A adesão ao PAT é a única forma de afastar a natureza salarial.',
            'risk_reason': 'Alto risco: muitas empresas fornecem alimentação sem adesão formal ao PAT e sem recolher os encargos, o que gera autuações expressivas em fiscalização. Verificar regularidade do cadastro PAT é essencial.',
        },
        'legal_basis': [{'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943, 'article': 'Art. 458, caput', 'is_primary': True,
            'excerpt': 'Além do pagamento em dinheiro, compreende-se no salário, para todos os efeitos legais, a alimentação, habitação, vestuário ou outras prestações in natura que a empresa, por força do contrato ou do costume, fornecer habitualmente ao empregado.'}],
    },

    # ── Licenças remuneradas ───────────────────────────────────────────────────
    {
        'name': 'Licença-Gala (Casamento)',
        'code': 'LGA001',
        'description': 'Afastamento remunerado de 3 dias consecutivos por motivo de casamento do empregado, sem desconto no salário.',
        'category': 'Proventos',
        'esocial_nature_code': '1010',
        'incidence': {
            'inss': True, 'fgts': True, 'irrf': True, 'risk_level': 'low',
            'risk_reason': 'Baixo risco: direito expresso no Art. 473 CLT. Os dias são remunerados normalmente, com incidência plena de encargos.',
        },
        'legal_basis': [{'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943, 'article': 'Art. 473, I', 'is_primary': True,
            'excerpt': 'O empregado poderá deixar de comparecer ao serviço sem prejuízo do salário: I — por 3 (três) dias, em virtude de casamento.'}],
    },
    {
        'name': 'Licença-Nojo (Luto)',
        'code': 'LNJ001',
        'description': 'Afastamento remunerado de 2 dias consecutivos por falecimento de cônjuge, pai, mãe, filho ou irmão.',
        'category': 'Proventos',
        'esocial_nature_code': '1010',
        'incidence': {
            'inss': True, 'fgts': True, 'irrf': True, 'risk_level': 'low',
            'risk_reason': 'Baixo risco: direito expresso no Art. 473 CLT. Os dias são remunerados normalmente como salário.',
        },
        'legal_basis': [{'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943, 'article': 'Art. 473, II', 'is_primary': True,
            'excerpt': 'O empregado poderá deixar de comparecer ao serviço sem prejuízo do salário: II — por 2 (dois) dias, por motivo de falecimento do cônjuge, ascendente, descendente, irmão ou pessoa que, declarada em sua carteira de trabalho, viva sob sua dependência econômica.'}],
    },
    {
        'name': 'Licença por Doação de Sangue (Art. 473 CLT)',
        'code': 'L473001',
        'description': 'Falta justificada de 1 dia por semestre para doação voluntária de sangue, sem desconto no salário.',
        'category': 'Proventos',
        'esocial_nature_code': '1010',
        'incidence': {
            'inss': True, 'fgts': True, 'irrf': True, 'risk_level': 'low',
            'risk_reason': 'Baixo risco: direito expresso no Art. 473 CLT. Os dias são remunerados normalmente como salário.',
        },
        'legal_basis': [{'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943, 'article': 'Art. 473, IV', 'is_primary': True,
            'excerpt': 'O empregado poderá deixar de comparecer ao serviço sem prejuízo do salário: IV — por 1 (um) dia, em cada 12 (doze) meses de trabalho, em caso de doação voluntária de sangue devidamente comprovada.'}],
    },

    # ── Afastamento por acidente ───────────────────────────────────────────────
    {
        'name': 'Primeiros 15 Dias — Acidente de Trabalho',
        'code': 'AF15A1',
        'description': 'Salário pago pelo empregador nos primeiros 15 dias de afastamento por acidente de trabalho. Inclui obrigação adicional de continuar depositando FGTS.',
        'category': 'Proventos',
        'esocial_nature_code': '1010',
        'incidence': {
            'inss': True, 'fgts': True, 'irrf': True, 'risk_level': 'low',
            'fgts_observation': 'O FGTS deve ser depositado nos primeiros 15 dias e continua obrigatório durante todo o afastamento acidentário (diferente do auxílio-doença comum).',
            'risk_reason': 'Baixo risco quanto à incidência, mas atenção: o FGTS continua obrigatório durante todo o período acidentário, erro frequente em empresas.',
        },
        'legal_basis': [{'norm_number': '8.213', 'norm_year': 1991, 'article': 'Art. 60, par. 3', 'is_primary': True,
            'excerpt': 'Durante os primeiros quinze dias consecutivos ao afastamento da atividade por motivo de acidente do trabalho, incumbirá à empresa pagar ao segurado empregado o seu salário integral.'}],
    },

    # ── Multas rescisórias ─────────────────────────────────────────────────────
    {
        'name': 'Multa Art. 467 CLT (Verbas Indisputadas)',
        'code': 'M467001',
        'description': 'Multa de 50% sobre as verbas rescisórias indisputadas não pagas até o comparecimento à Justiça do Trabalho.',
        'category': 'Informativos',
        'esocial_nature_code': '1360',
        'incidence': {
            'inss': False, 'fgts': False, 'irrf': False, 'risk_level': 'low',
            'inss_observation': 'Natureza indenizatória/punitiva — não integra o salário de contribuição.',
            'risk_reason': 'Baixo risco quanto à incidência (não há encargos). O risco está na própria geração da multa: atraso no pagamento das verbas rescisórias expõe a empresa a esta penalidade.',
        },
        'legal_basis': [{'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943, 'article': 'Art. 467', 'is_primary': True,
            'excerpt': 'Em caso de rescisão de contrato de trabalho, havendo controvérsia sobre o montante das verbas rescisórias, o empregador é obrigado a pagar ao trabalhador, à data do comparecimento à Justiça Trabalhista, a parte incontroversa dessas verbas, sob pena de pagá-las acrescidas de cinquenta por cento.'}],
    },
    {
        'name': 'Multa Art. 477 CLT (Atraso na Quitação)',
        'code': 'M477001',
        'description': 'Multa equivalente a 1 salário do empregado por atraso no pagamento das verbas rescisórias além do prazo legal (10 dias corridos).',
        'category': 'Informativos',
        'esocial_nature_code': '1360',
        'incidence': {
            'inss': False, 'fgts': False, 'irrf': False, 'risk_level': 'low',
            'inss_observation': 'Natureza indenizatória — não há incidência de INSS, FGTS ou IRRF sobre a multa.',
            'risk_reason': 'Baixo risco de encargos, mas a multa em si é frequentemente aplicada em fiscalização — prazo de 10 dias para quitação deve ser rigorosamente observado.',
        },
        'legal_basis': [{'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943, 'article': 'Art. 477, par. 8', 'is_primary': True,
            'excerpt': 'A inobservância do prazo estabelecido no § 6.º sujeitará o infrator ao pagamento de multa em favor do empregado, em valor equivalente ao seu salário, devidamente corrigido, salvo quando, comprovadamente, o trabalhador der causa à mora.'}],
    },

    # ── Indenizações de estabilidade ───────────────────────────────────────────
    {
        'name': 'Indenização de Estabilidade — Gestante',
        'code': 'IEG001',
        'description': 'Indenização devida à empregada gestante dispensada sem justa causa, correspondente aos salários do período de estabilidade.',
        'category': 'Informativos',
        'esocial_nature_code': '1350',
        'incidence': {
            'inss': False, 'fgts': False, 'irrf': False, 'risk_level': 'high',
            'inss_observation': 'Natureza indenizatória — não integra o salário de contribuição conforme entendimento predominante do TST e RFB (Nota COSIT 07/2013).',
            'irrf_observation': 'A indenização substitutiva da estabilidade não é tributável pelo IRRF (RIR/2018, Art. 39, XX).',
            'risk_reason': 'Alto risco processual: a estabilidade da gestante ocorre desde a confirmação da gravidez até 5 meses após o parto (Súmula 244 TST). A empresa muitas vezes não sabe da gravidez, mas a dispensa é considerada ilegal. Fundamental confirmar estado gestacional antes da demissão.',
        },
        'legal_basis': [{'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943, 'article': 'Art. 10, II, b, ADCT c/c Sumula 244 TST', 'is_primary': True,
            'excerpt': 'Fica vedada a dispensa arbitrária ou sem justa causa da empregada gestante, desde a confirmação da gravidez até cinco meses após o parto.'}],
    },
    {
        'name': 'Indenização de Estabilidade — Cipeiro',
        'code': 'IEC001',
        'description': 'Indenização devida ao membro da CIPA dispensado sem justa causa durante o período de estabilidade (candidatura + mandato + 1 ano após).',
        'category': 'Informativos',
        'esocial_nature_code': '1350',
        'incidence': {
            'inss': False, 'fgts': False, 'irrf': False, 'risk_level': 'medium',
            'inss_observation': 'Natureza indenizatória — não integra a base de contribuição previdenciária.',
            'risk_reason': 'Risco médio: a estabilidade se estende a candidatos não eleitos e ao delegado sindical. Empresas frequentemente ignoram a estabilidade na candidatura, gerando passivo relevante.',
        },
        'legal_basis': [{'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943, 'article': 'Art. 10, II, a, ADCT', 'is_primary': True,
            'excerpt': 'Fica vedada a dispensa arbitrária ou sem justa causa do empregado eleito para cargos de direção de comissões internas de prevenção de acidentes, desde o registro de sua candidatura até um ano após o final de seu mandato.'}],
    },

    # ── Pró-labore e Stock Options ─────────────────────────────────────────────
    {
        'name': 'Pró-Labore — Sócio-Administrador',
        'code': 'PRO001',
        'description': 'Remuneração dos sócios que exercem funções de administração ou direção na empresa. Sujeito a INSS e IRRF, mas não ao FGTS.',
        'category': 'Proventos',
        'esocial_nature_code': '9300',
        'incidence': {
            'inss': True, 'fgts': False, 'irrf': True, 'risk_level': 'medium',
            'inss_observation': 'Incide INSS sobre o pró-labore: o sócio-administrador é segurado obrigatório na categoria Contribuinte Individual (Art. 12, V, f, Lei 8.212). Alíquota de 20% para empresa + 11% do sócio.',
            'fgts_observation': 'Não há vínculo empregatício, portanto o FGTS não é devido.',
            'irrf_observation': 'Incide IRRF pela tabela progressiva, aplicado na fonte pela empresa.',
            'risk_reason': 'Risco médio: sócios sem pró-labore formalmente estabelecido podem ser autuados pela Receita Federal, que presume remuneração. Também há risco de descaracterização da distribuição de lucros quando o pró-labore é muito baixo.',
        },
        'legal_basis': [{'norm_number': '8.212', 'norm_year': 1991, 'article': 'Art. 12, V, f', 'is_primary': True,
            'excerpt': 'Considera-se empregado o sócio administrador de firma individual ou empresa por cotas de responsabilidade limitada, pelo trabalho que nela exerce, em caráter habitual.'}],
    },
    {
        'name': 'Stock Options — Exercício de Opção',
        'code': 'STO001',
        'description': 'Ganho auferido pelo empregado no exercício de opção de compra de ações da empresa por preço inferior ao de mercado.',
        'category': 'Proventos',
        'esocial_nature_code': '1260',
        'incidence': {
            'inss': False, 'fgts': False, 'irrf': True, 'risk_level': 'high',
            'inss_observation': 'Após a IN RFB 2.180/2024, o ganho no exercício das opções é tributado pelo IRRF como rendimento do trabalho — a questão INSS permanece controversa entre RFB (sim) e TST (não, natureza mercantil).',
            'irrf_observation': 'Conforme IN RFB 2.180/2024, o ganho líquido (diferença entre preço de exercício e preço de mercado) é tributado como rendimento do trabalho no mês do exercício.',
            'risk_reason': 'Alto risco: a IN 2.180/2024 criou nova tese tributária que ainda está sendo questionada judicialmente. Empresas que mantinham stock options como "mercantis" precisam revisar tratamento. Divergência ativa entre RFB e TST sobre incidência de INSS.',
        },
        'legal_basis': [{'norm_number': '2.180', 'norm_year': 2024, 'article': 'Art. 3 e 4', 'is_primary': True,
            'excerpt': 'O ganho auferido pelo beneficiário de plano de opção de compra de ações de pessoas jurídicas, na data do exercício da opção de compra, será tributado como rendimento do trabalho.'}],
    },

    # ── Desconto previdência complementar ─────────────────────────────────────
    {
        'name': 'Previdência Complementar — Desconto Empregado',
        'code': 'PVE001',
        'description': 'Valor descontado do empregado como contribuição ao plano de previdência complementar patrocinado pela empresa.',
        'category': 'Descontos',
        'esocial_nature_code': '9190',
        'incidence': {
            'inss': False, 'fgts': False, 'irrf': False, 'risk_level': 'low',
            'irrf_observation': 'Contribuições a entidades de previdência privada são dedutíveis da base do IRRF até 12% da renda tributável anual (Lei 9.532/1997), portanto reduzem a base e não representam tributação adicional.',
            'risk_reason': 'Baixo risco: desconto pacífico quando feito em plano devidamente registrado na SUSEP/Previc. Atenção para o limite de 12% para a dedução no IRRF.',
        },
        'legal_basis': [{'norm_number': '9.532', 'norm_year': 1997, 'article': 'Art. 11', 'is_primary': True,
            'excerpt': 'A partir do ano-calendário de 1998, as contribuições da pessoa física a planos de previdência privada pagos ou creditados a entidades de previdência privada domiciliadas no País são dedutíveis na determinação da base de cálculo do imposto de renda não excedente a 12% do total dos rendimentos computados na determinação da base de cálculo do imposto devido na declaração de rendimentos.'}],
    },

    # ── Complemento e verbas de férias ─────────────────────────────────────────
    {
        'name': 'Complemento Salarial sobre Auxílio-Doença',
        'code': 'AUC001',
        'description': 'Diferença paga pela empresa entre o benefício do INSS e o salário integral do empregado, por ato normativo ou norma coletiva.',
        'category': 'Proventos',
        'esocial_nature_code': '1010',
        'incidence': {
            'inss': True, 'fgts': True, 'irrf': True, 'risk_level': 'medium',
            'inss_observation': 'O complemento tem natureza salarial — integra o salário de contribuição e o FGTS, já que representa remuneração paga pelo empregador.',
            'risk_reason': 'Risco médio: muitas empresas confundem o complemento (tributável) com o benefício INSS (não tributável). O complemento pago pela empresa é verba salarial plena. Erros nessa distinção geram autuações significativas.',
        },
        'legal_basis': [{'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943, 'article': 'Art. 457, caput', 'is_primary': True,
            'excerpt': 'Compreendem-se na remuneração do empregado, para todos os efeitos legais, além do salário devido e pago diretamente pelo empregador, como contraprestação do serviço, todos os valores habituais recebidos.'}],
    },
    {
        'name': 'Dobra de Férias (Art. 137 CLT)',
        'code': 'FED001',
        'description': 'Pagamento em dobro das férias não concedidas no período concessivo, acrescido do adicional de 1/3 sobre o total dobrado.',
        'category': 'Informativos',
        'esocial_nature_code': '1350',
        'incidence': {
            'inss': False, 'fgts': False, 'irrf': False, 'risk_level': 'medium',
            'inss_observation': 'A dobra de férias tem natureza indenizatória (sanção pelo descumprimento do prazo) — não integra o salário de contribuição (Decisão TST e entendimento RFB).',
            'risk_reason': 'Risco médio: embora a natureza indenizatória seja predominante, há fiscalizações que autuam a dobra como rendimento salarial. Recomenda-se segregar contabilmente a parte regular (tributável) da dobra (indenizatória).',
        },
        'legal_basis': [{'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943, 'article': 'Art. 137', 'is_primary': True,
            'excerpt': 'Ao empregador que não conceder as férias dentro do período a que se refere o art. 134, será obrigado a pagar-as em dobro.'}],
    },

    # ── Base informativa — RAT/FAP ─────────────────────────────────────────────
    {
        'name': 'RAT/FAP — Contribuição Acidentária',
        'code': 'RAT001',
        'description': 'Contribuição patronal ao SAT (Seguro Acidente do Trabalho), calculada sobre a folha de salários, com alíquota ajustada pelo FAP (0,5% a 6%).',
        'category': 'Bases de Cálculo',
        'esocial_nature_code': '9100',
        'incidence': {
            'inss': False, 'fgts': False, 'irrf': False, 'risk_level': 'medium',
            'inss_observation': 'Contribuição patronal (empresa paga) calculada sobre o total das remunerações pagas. Não é desconto do empregado. Alíquota base: 1%, 2% ou 3%, multiplicada pelo FAP (0,5 a 2,0 — divulgado anualmente pelo INSS).',
            'risk_reason': 'Risco médio: muitas empresas aplicam alíquota incorreta do RAT ou não atualizam o FAP anualmente, gerando diferenças de recolhimento. O CNAE determina a alíquota base — alterações na atividade principal devem refletir no CNAE e no RAT.',
        },
        'legal_basis': [{'norm_number': '8.212', 'norm_year': 1991, 'article': 'Art. 22, II', 'is_primary': True,
            'excerpt': 'A contribuição a cargo da empresa, destinada ao financiamento dos benefícios concedidos em razão do grau de incidência de incapacidade laborativa decorrente dos riscos ambientais do trabalho, é de 1%, 2% ou 3%, conforme disponha o regulamento, em razão do grau de risco de acidentes do trabalho.'}],
    },
]


class Command(BaseCommand):
    help = 'Seed v1.2 — adiciona 20 rubricas (quebra de caixa, anuênio, stock options, multas, indenizações, etc.)'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        from apps.catalog.models import Category, EsocialNature, Rubric
        from apps.legislation.models import LegalNorm, LegalBasis
        from apps.engine.models import Incidence

        self.stdout.write('Criando naturezas eSocial v1.2...')
        for data in V12_NATURES:
            EsocialNature.objects.get_or_create(
                code=data['code'],
                defaults={
                    'description': data['description'],
                    'is_salary_nature': data['is_salary_nature'],
                }
            )

        self.stdout.write('Criando normas legais v1.2...')
        norm_map = {}
        for norm in LegalNorm.objects.all():
            norm_map[(norm.number, norm.year)] = norm

        for data in V12_NORMS:
            norm, _ = LegalNorm.objects.get_or_create(
                number=data['number'],
                year=data['year'],
                defaults=data
            )
            norm_map[(data['number'], data['year'])] = norm

        self.stdout.write('Criando rubricas v1.2...')
        created_count = 0
        for r in RUBRICAS_V12:
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
                        'iss': inc_data.get('iss', False),
                        'inss_observation': inc_data.get('inss_observation', ''),
                        'fgts_observation': inc_data.get('fgts_observation', ''),
                        'irrf_observation': inc_data.get('irrf_observation', ''),
                        'iss_observation': inc_data.get('iss_observation', ''),
                        'risk_level': inc_data.get('risk_level', 'low'),
                        'risk_reason': inc_data.get('risk_reason', ''),
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
