"""
Seed v1.4 — 25 rubricas cobrindo segmentos avançados:
  - Retenções na fonte (ISS, PIS/COFINS, CSLL, IRRF serviços)
  - Segmento rural (Trabalhador Rural, Funrural)
  - Construção civil (trabalhador avulso, FGTS complementar)
  - Cooperativas (distribuição de sobras, INSS sobre serviços)
  - Adicionais de norma coletiva (fronteira, honorários diretores, licença CCT)
  - Benefícios modernos (Gympass, EAP, carro/celular para uso pessoal)
  - Contratos e rescisões específicas (abandono de emprego, contrato a prazo)
  - Gratificação convencional (14º salário)
  - Jetons — conselho de administração

Execute com: python manage.py seed_v14_rubricas
"""
from django.core.management.base import BaseCommand
from django.db import transaction


V14_NATURES = [
    {'code': '5100', 'description': 'Carro Empresa para Uso Pessoal (In Natura)', 'is_salary_nature': True},
    {'code': '5110', 'description': 'Celular / Plano Corporativo para Uso Pessoal (In Natura)', 'is_salary_nature': True},
    {'code': '5120', 'description': 'Gympass / Beneficio Bem-Estar (Empresa)', 'is_salary_nature': False},
    {'code': '5130', 'description': 'Programa de Assistencia ao Empregado (EAP)', 'is_salary_nature': False},
    {'code': '1800', 'description': 'Trabalhador Rural — Salario', 'is_salary_nature': True},
    {'code': '1810', 'description': 'Funrural — Contribuicao s/ Comercializacao (Informativo)', 'is_salary_nature': False},
    {'code': '1820', 'description': 'Construcao Civil — Trabalhador Avulso', 'is_salary_nature': True},
    {'code': '1830', 'description': 'Cooperado — Distribuicao de Sobras', 'is_salary_nature': False},
    {'code': '9400', 'description': 'ISS Retido na Fonte pelo Tomador', 'is_salary_nature': False},
    {'code': '9410', 'description': 'PIS/COFINS Retidos na Fonte (IN 1.234/2012)', 'is_salary_nature': False},
    {'code': '9420', 'description': 'CSLL Retida na Fonte', 'is_salary_nature': False},
    {'code': '9430', 'description': 'IRRF Retido na Fonte — Servicos de PF/Autonomo', 'is_salary_nature': False},
    {'code': '9440', 'description': 'INSS Retido na Fonte — Cooperado (15%)', 'is_salary_nature': False},
    {'code': '9500', 'description': 'Adicional de Fronteira (Art. 463 CLT)', 'is_salary_nature': True},
    {'code': '9510', 'description': 'Honorarios de Diretores Sem Vinculo Empregaticio', 'is_salary_nature': False},
    {'code': '9520', 'description': 'Jetons — Conselho de Administracao', 'is_salary_nature': False},
    {'code': '1840', 'description': 'Construcao Civil — FGTS Complementar 2%', 'is_salary_nature': False},
    {'code': '1100', 'description': '14 Salario (Gratificacao em Norma Coletiva)', 'is_salary_nature': True},
]

V14_NORMS = [
    {
        'norm_type': 'lei', 'number': '8.870', 'year': 1994,
        'title': 'Lei 8.870/1994 — Contribuicao do Empregador Rural',
        'official_link': 'https://www.planalto.gov.br/ccivil_03/leis/l8870.htm',
    },
    {
        'norm_type': 'in', 'number': '1.234', 'year': 2012,
        'title': 'IN RFB 1.234/2012 — Retencoes PIS/COFINS/CSLL na Fonte',
        'official_link': 'https://normas.receita.fazenda.gov.br/sijut2consulta/link.action?idAto=37847',
    },
    {
        'norm_type': 'lc', 'number': '5.764', 'year': 1971,
        'title': 'Lei 5.764/1971 — Cooperativas (Politica Nacional do Cooperativismo)',
        'official_link': 'https://www.planalto.gov.br/ccivil_03/leis/l5764.htm',
    },
    {
        'norm_type': 'lei', 'number': '9.711', 'year': 1998,
        'title': 'Lei 9.711/1998 — INSS sobre Cessao de Mao de Obra e Cooperativas',
        'official_link': 'https://www.planalto.gov.br/ccivil_03/leis/l9711.htm',
    },
]

RUBRICAS_V14 = [

    # ── Retenções na fonte ────────────────────────────────────────────────────
    {
        'name': 'ISS Retido na Fonte pelo Tomador',
        'code': 'ISS001',
        'description': 'ISS retido pelo tomador de serviços quando obrigado por legislação municipal. Incide sobre o preço do serviço, com alíquota de 2% a 5% conforme a municipalidade.',
        'category': 'Informativos',
        'esocial_nature_code': '9400',
        'incidence': {
            'inss': False, 'fgts': False, 'irrf': False, 'iss': True, 'risk_level': 'medium',
            'iss_observation': 'A retenção do ISS na fonte depende de legislação do município do tomador. Alíquota varia de 2% a 5% (LC 116/2003). Alguns municípios não autorizam retenção para todos os serviços.',
            'risk_reason': 'Risco médio: o tomador que não reter o ISS quando obrigado responde solidariamente pelo tributo. A determinação do município competente para o ISS (local do estabelecimento prestador ou do serviço) varia conforme o tipo de serviço — LC 116/2003 lista os casos de exceção à regra do prestador.',
        },
        'legal_basis': [{'norm_number': '116', 'norm_year': 2003, 'article': 'Art. 6, par. 1', 'is_primary': True,
            'excerpt': 'Os municípios e o Distrito Federal, mediante lei, poderão atribuir de modo expresso a responsabilidade pelo crédito tributário a terceira pessoa, vinculada ao fato gerador da respectiva obrigação, excluindo a responsabilidade do contribuinte.'}],
    },
    {
        'name': 'PIS/COFINS Retidos na Fonte',
        'code': 'PIS001',
        'description': 'Retenção de PIS (0,65%) e COFINS (3%) na fonte, aplicável a pagamentos efetuados por pessoas jurídicas a outras pessoas jurídicas por serviços discriminados na IN RFB 1.234/2012.',
        'category': 'Informativos',
        'esocial_nature_code': '9410',
        'incidence': {
            'inss': False, 'fgts': False, 'irrf': False, 'risk_level': 'medium',
            'risk_reason': 'Risco médio: tomadores que deixam de reter PIS/COFINS quando obrigados ficam sujeitos a multa de 75% sobre o tributo não retido. A lista de serviços sujeitos à retenção (Anexo I da IN 1.234) deve ser verificada para cada tipo de serviço contratado.',
        },
        'legal_basis': [{'norm_number': '1.234', 'norm_year': 2012, 'article': 'Art. 1', 'is_primary': True,
            'excerpt': 'Ficam obrigadas a efetuar as retenções na fonte do IRPJ, da CSLL, da Cofins e da Contribuição para o PIS/Pasep, a que se refere o Art. 64 da Lei 9.430/1996, as pessoas jurídicas que efetuarem pagamentos a outras pessoas jurídicas de direito privado, pela prestação de serviços relacionados no Anexo I desta Instrução Normativa.'}],
    },
    {
        'name': 'CSLL Retida na Fonte',
        'code': 'CSLL01',
        'description': 'Retenção de CSLL (1%) na fonte sobre pagamentos a pessoas jurídicas por serviços sujeitos à IN RFB 1.234/2012. Recolhida junto com PIS/COFINS e IRPJ na mesma guia DARF.',
        'category': 'Informativos',
        'esocial_nature_code': '9420',
        'incidence': {
            'inss': False, 'fgts': False, 'irrf': False, 'risk_level': 'medium',
            'risk_reason': 'Risco médio: idêntico ao PIS/COFINS. A CSLL é retida concomitantemente. O DARF único concentra IRPJ + CSLL + PIS + COFINS. Código DARF: 5952 (serviços em geral) ou específico conforme o serviço.',
        },
        'legal_basis': [{'norm_number': '1.234', 'norm_year': 2012, 'article': 'Art. 2, III', 'is_primary': True,
            'excerpt': 'As retenções de que trata o art. 1° serão efetuadas sem prejuízo do Imposto sobre a Renda e da Contribuição Social sobre o Lucro Líquido, em alíquota de 1% sobre os pagamentos efetuados às pessoas jurídicas.'}],
    },
    {
        'name': 'IRRF Retido na Fonte — Serviços de Autônomo',
        'code': 'IRF001',
        'description': 'Retenção de IRRF pelo tomador sobre pagamentos a trabalhadores autônomos (PF) pela prestação de serviços, calculada sobre a base de cálculo após dedução do INSS.',
        'category': 'Informativos',
        'esocial_nature_code': '9430',
        'incidence': {
            'inss': False, 'fgts': False, 'irrf': True, 'risk_level': 'medium',
            'irrf_observation': 'Alíquota conforme tabela progressiva mensal. A base é o valor bruto menos a contribuição ao INSS (autônomo contribuinte individual: 20% ou alíquota simplificada).',
            'risk_reason': 'Risco médio: tomadores que não retêm o IRRF de autônomos respondem conjuntamente pelo imposto não recolhido. É também obrigatório declarar os pagamentos na DIRF. O autônomo que recebe sem retenção pode ter surpresa na DIRPF.',
        },
        'legal_basis': [{'norm_number': '8.212', 'norm_year': 1991, 'article': 'Art. 45 c/c Decreto 9.580/2018 Art. 720', 'is_primary': True,
            'excerpt': 'A fonte pagadora é obrigada a calcular e a reter o imposto de renda na fonte no momento do pagamento, inclusive nos adiantamentos a qualquer título, sobre os rendimentos tributáveis do trabalho assalariado ou não.'}],
    },

    # ── Segmento rural ────────────────────────────────────────────────────────
    {
        'name': 'Trabalhador Rural — Salário',
        'code': 'RUR001',
        'description': 'Salário do empregado rural. O INSS patronal do empregador rural segue regra diferenciada (2,5% s/ receita bruta da comercialização) em vez da alíquota normal de 20%.',
        'category': 'Proventos',
        'esocial_nature_code': '1800',
        'incidence': {
            'inss': True, 'fgts': True, 'irrf': True, 'risk_level': 'medium',
            'inss_observation': 'O INSS do empregado rural é descontado normalmente (11% ou tabela). O empregador rural (pessoa física ou agroindústria) recolhe 2,5% sobre a receita bruta da comercialização no lugar dos 20% patronais — regra específica do Funrural.',
            'risk_reason': 'Risco médio: a definição de empregador rural (Pessoa Física, Pessoa Jurídica agroindústria ou empresa agroindustrial) determina a alíquota. Agroindústrias que contratam empregados urbanos e rurais na mesma folha precisam segregar as bases. Liminar do STF (ADC 18) ainda gera incerteza sobre a constitucionalidade do Funrural para PJ.',
        },
        'legal_basis': [{'norm_number': '8.870', 'norm_year': 1994, 'article': 'Art. 25', 'is_primary': True,
            'excerpt': 'Contribui com a alíquota de 2% da receita bruta proveniente da comercialização da sua produção o empregador rural pessoa física.'}],
    },
    {
        'name': 'Funrural — Contribuição s/ Comercialização',
        'code': 'FUN001',
        'description': 'Contribuição previdenciária patronal do empregador rural calculada sobre a receita bruta da comercialização da produção (2,5% para PF; 1,7% para PJ agroindústria).',
        'category': 'Informativos',
        'esocial_nature_code': '1810',
        'incidence': {
            'inss': False, 'fgts': False, 'irrf': False, 'risk_level': 'high',
            'inss_observation': 'Encargo patronal rural — substitui o INSS sobre a folha. A base é a receita bruta da comercialização, não a folha de salários. O adquirente da produção rural de PF é responsável pela retenção e recolhimento.',
            'risk_reason': 'Alto risco: tese tributária controversa — o Funrural foi declarado inconstitucional pelo STF em 2010 (RE 363.852) e depois constitucional novamente para novos fatos geradores. Produtores rurais que suspenderam o recolhimento durante a discussão acumularam passivo. É fundamental verificar o status atual e o tipo de produtor (PF, PJ, cooperativa).',
        },
        'legal_basis': [{'norm_number': '8.870', 'norm_year': 1994, 'article': 'Art. 25, I e II', 'is_primary': True,
            'excerpt': 'A contribuição do empregador rural, pessoa jurídica, é de 2% sobre a receita bruta proveniente da comercialização da produção rural, destinada ao custeio das prestações previdenciárias.'}],
    },

    # ── Construção civil ──────────────────────────────────────────────────────
    {
        'name': 'Construção Civil — Trabalhador Avulso',
        'code': 'CCI001',
        'description': 'Remuneração do trabalhador avulso da construção civil, intermediado pelo Sindicato ou OGMO. O INSS patronal é recolhido pela empresa tomadora à alíquota de 20%, sem vínculo direto.',
        'category': 'Proventos',
        'esocial_nature_code': '1820',
        'incidence': {
            'inss': True, 'fgts': False, 'irrf': True, 'risk_level': 'high',
            'inss_observation': 'O INSS (contribuinte individual/avulso) é descontado do bruto. O FGTS do avulso é recolhido pelo sindicato — a empresa não deposita FGTS diretamente.',
            'fgts_observation': 'O FGTS do trabalhador avulso é gerido pelo sindicato ou OGMO. A empresa não realiza depósito direto — apenas repassa o percentual ao intermediário.',
            'risk_reason': 'Alto risco: a distinção entre trabalhador avulso (intermediado por sindicato/OGMO) e empregado da construção civil gera frequentes litígios. O mau enquadramento impõe FGTS retroativo, aviso prévio e verbas rescisórias. Exigir o Certificado de Matrícula CEI/CNO da obra também é obrigação.',
        },
        'legal_basis': [{'norm_number': '8.212', 'norm_year': 1991, 'article': 'Art. 15, par. 4', 'is_primary': True,
            'excerpt': 'O FGTS do trabalhador avulso é depositado pelo sindicato ou órgão gestor de mão de obra na conta vinculada, em nome do trabalhador, no prazo e nas condições definidos pelo Conselho Curador.'}],
    },
    {
        'name': 'Construção Civil — FGTS Complementar 2%',
        'code': 'DEA001',
        'description': 'Depósito adicional de FGTS de 2% a cargo do empregador da construção civil, incidente sobre a base de cálculo normal, totalizando 10% (8% + 2%).',
        'category': 'Informativos',
        'esocial_nature_code': '1840',
        'incidence': {
            'inss': False, 'fgts': False, 'irrf': False, 'risk_level': 'low',
            'fgts_observation': 'O 2% adicional é encargo exclusivo do empregador — não desconta do empregado. O trabalhador de construção civil tem 10% total de FGTS em vez dos 8% normais.',
            'risk_reason': 'Baixo risco de incidência. O risco está em esquecer o depósito complementar — sistemas de folha genéricos frequentemente calculam só 8%, gerando passivo de FGTS no final da obra.',
        },
        'legal_basis': [{'norm_number': '8.036', 'norm_year': 1990, 'article': 'Art. 15, par. 3', 'is_primary': True,
            'excerpt': 'Fica facultado ao empregador equiparar seus empregados aos trabalhadores avulsos a que se refere o inciso VI do art. 9° da Lei 8.213/1991, para fins de recolhimento do FGTS.'}],
    },

    # ── Cooperativas ──────────────────────────────────────────────────────────
    {
        'name': 'Cooperado — Distribuição de Sobras',
        'code': 'COO001',
        'description': 'Distribuição do resultado líquido da cooperativa aos cooperados, proporcional às operações realizadas. Pode ser isenta de IRRF até determinado limite, conforme natureza da cooperativa.',
        'category': 'Informativos',
        'esocial_nature_code': '1830',
        'incidence': {
            'inss': False, 'fgts': False, 'irrf': False, 'risk_level': 'medium',
            'irrf_observation': 'Distribuição de sobras de cooperativas de trabalho: pode ser tributável pelo IRRF se configurado como rendimento do trabalho. Em cooperativas de consumo/crédito, as sobras geralmente são isentas. Consultar advogado tributarista.',
            'risk_reason': 'Risco médio: a natureza tributária das sobras distribuídas varia pelo tipo de cooperativa (trabalho, consumo, crédito, habitacional). Cooperativas de trabalho frequentemente distribuem "antecipação de sobras" que podem ser recaracterizadas como salário pela RFB.',
        },
        'legal_basis': [{'norm_number': '5.764', 'norm_year': 1971, 'article': 'Art. 89', 'is_primary': True,
            'excerpt': 'Os resultados das operações das cooperativas em cada exercício serão denominados sobras ou perdas, conforme o caso, e serão distribuídos ou suportados pelos cooperados.'}],
    },
    {
        'name': 'Cooperativa — INSS Retido na Fonte (15%)',
        'code': 'COI001',
        'description': 'Retenção de 15% do valor bruto da nota fiscal de serviços prestados por cooperativa de trabalho, a ser recolhido pelo tomador para custeio do INSS dos cooperados.',
        'category': 'Informativos',
        'esocial_nature_code': '9440',
        'incidence': {
            'inss': True, 'fgts': False, 'irrf': False, 'risk_level': 'medium',
            'inss_observation': 'O tomador de serviços de cooperativa de trabalho retém 15% do valor bruto da NF e recolhe em nome da cooperativa. A cooperativa, por sua vez, desconta do cooperado a contribuição individual correspondente.',
            'risk_reason': 'Risco médio: o tomador que não efetua a retenção dos 15% torna-se responsável solidário pelo pagamento. A base de cálculo é o valor total da nota fiscal, incluindo incidentes. Cooperativas irregulares ou que não repassam o INSS aos cooperados geram passivo para o tomador.',
        },
        'legal_basis': [{'norm_number': '9.711', 'norm_year': 1998, 'article': 'Art. 22, IV', 'is_primary': True,
            'excerpt': 'A empresa contratante de serviços executados por trabalhadores avulsos, admitidos ou não por intermédio de sindicatos, fica obrigada a fornecer, mensalmente, ao órgão gestor de mão-de-obra ou ao sindicato, informações relativas a esses trabalhadores.'}],
    },

    # ── Adicionais de norma coletiva / Segmentos ──────────────────────────────
    {
        'name': 'Adicional de Fronteira (Art. 463 CLT)',
        'code': 'AFT001',
        'description': 'Adicional de 25% sobre o salário devido aos empregados que trabalham em localidades fronteiriças ou com transferência compulsória para regiões de elevado custo de vida.',
        'category': 'Proventos',
        'esocial_nature_code': '9500',
        'incidence': {
            'inss': True, 'fgts': True, 'irrf': True, 'risk_level': 'low',
            'risk_reason': 'Baixo risco: adicional com previsão legal expressa. Integra o salário de contribuição e o FGTS. Atenção para a comprovação da transferência compulsória (não se aplica a empregados que se mudaram voluntariamente).',
        },
        'legal_basis': [{'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943, 'article': 'Art. 469 e 470', 'is_primary': True,
            'excerpt': 'Ao empregado transferido, por necessidade de serviço, para localidade diversa da que resultar do contrato, assegura-se, enquanto durar essa situação, um adicional nunca inferior a vinte e cinco por cento dos salários que recebia.'}],
    },
    {
        'name': 'Honorários de Diretores Sem Vínculo Empregatício',
        'code': 'HOD001',
        'description': 'Remuneração de diretores eleitos pelo conselho de administração ou assembléia, sem vínculo empregatício. Sujeito ao INSS como contribuinte individual e ao IRRF.',
        'category': 'Proventos',
        'esocial_nature_code': '9510',
        'incidence': {
            'inss': True, 'fgts': False, 'irrf': True, 'risk_level': 'medium',
            'inss_observation': 'O diretor sem vínculo empregatício é segurado obrigatório como contribuinte individual. A empresa retém 11% (ou a alíquota do INSS) sobre os honorários e recolhe mais 20% como patronal.',
            'fgts_observation': 'Não há FGTS para diretores sem vínculo empregatício.',
            'risk_reason': 'Risco médio: a configuração do vínculo empregatício de diretores é frequentemente questionada pela Fiscalização e pelo TST. Se o diretor foi empregado e depois promovido a diretor estatutário sem ruptura do vínculo original, o FGTS pode ser devido pelo período. Documentação societária completa é essencial.',
        },
        'legal_basis': [{'norm_number': '8.212', 'norm_year': 1991, 'article': 'Art. 12, V, f', 'is_primary': True,
            'excerpt': 'Considera-se contribuinte individual o diretor não empregado de sociedades anônimas que receba remuneração decorrente do exercício de suas funções.'}],
    },
    {
        'name': 'Licença Remunerada por Norma Coletiva',
        'code': 'LIC001',
        'description': 'Licença remunerada prevista exclusivamente em acordo ou convenção coletiva de trabalho, com período e remuneração superiores ao mínimo legal.',
        'category': 'Proventos',
        'esocial_nature_code': '1010',
        'incidence': {
            'inss': True, 'fgts': True, 'irrf': True, 'risk_level': 'medium',
            'inss_observation': 'A licença remunerada convencional tem natureza salarial e integra a base de contribuição dos encargos.',
            'risk_reason': 'Risco médio: a validade da norma coletiva deve ser verificada (vigência, abrangência geográfica e categoria profissional). Normas coletivas vencidas não amparam mais a obrigação — mas o empregado que já gozou da licença não precisa devolver.',
        },
        'legal_basis': [{'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943, 'article': 'Art. 611-A, III', 'is_primary': True,
            'excerpt': 'A convenção coletiva e o acordo coletivo de trabalho têm prevalência sobre a lei quando dispuserem sobre: III — banco de horas anual; IV — intervalo intrajornada, respeitado o limite mínimo de trinta minutos.'}],
    },
    {
        'name': 'Adicional de Capacitação/Certificação (Norma Coletiva)',
        'code': 'ACA001',
        'description': 'Valor adicional ao salário pago aos empregados que obtêm certificações técnicas ou cursos previstos em norma coletiva ou regulamento interno como condição de progressão.',
        'category': 'Proventos',
        'esocial_nature_code': '1230',
        'incidence': {
            'inss': True, 'fgts': True, 'irrf': True, 'risk_level': 'low',
            'risk_reason': 'Baixo risco: tem natureza salarial por ser pago em caráter habitual como contraprestação ao trabalho qualificado. Verificar se a norma coletiva ou regulamento ainda está vigente para evitar supressão abrupta.',
        },
        'legal_basis': [{'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943, 'article': 'Art. 457, par. 1', 'is_primary': True,
            'excerpt': 'Integram o salário a importância fixa estipulada, as gratificações legais e as comissões pagas pelo empregador.'}],
    },

    # ── Benefícios modernos ───────────────────────────────────────────────────
    {
        'name': 'Gympass / Wellhub — Benefício Bem-Estar',
        'code': 'GYM001',
        'description': 'Benefício de bem-estar físico e mental (academias, psicólogos, meditação) oferecido por plataformas como Gympass/Wellhub. Natureza controversa: salário in natura ou indenizatório?',
        'category': 'Informativos',
        'esocial_nature_code': '5120',
        'incidence': {
            'inss': False, 'fgts': False, 'irrf': False, 'risk_level': 'medium',
            'inss_observation': 'Posição majoritária atual: por ser ligado à saúde e bem-estar do trabalhador (semelhante ao plano de saúde), não integra o salário de contribuição. Porém, a Receita Federal não editou norma específica sobre o tema.',
            'risk_reason': 'Risco médio: ausência de norma específica sobre tributação de benefícios de bem-estar. Empresas conservadoras tributam como in natura salarial; liberais equiparam ao plano de saúde (não salarial). A tendência é pela não incidência, mas há risco de autuação fiscal.',
        },
        'legal_basis': [{'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943, 'article': 'Art. 458, par. 2, IV — analogia', 'is_primary': True,
            'excerpt': 'Não serão considerados como salário as assistências médica, hospitalar e odontológica prestadas diretamente ou mediante seguro-saúde, bem como aquelas de natureza correlata voltadas à saúde do trabalhador.'}],
    },
    {
        'name': 'EAP — Programa de Assistência ao Empregado',
        'code': 'EAP001',
        'description': 'Benefício corporativo que oferece atendimento psicológico, jurídico, financeiro e social aos empregados. Não tem natureza salarial por ser voltado exclusivamente ao bem-estar funcional.',
        'category': 'Informativos',
        'esocial_nature_code': '5130',
        'incidence': {
            'inss': False, 'fgts': False, 'irrf': False, 'risk_level': 'low',
            'risk_reason': 'Baixo risco: benefício de natureza assistencial/indenizatória análogo ao plano de saúde. Não há disposição explícita sobre EAP, mas o entendimento doutrinário é pela não incidência por ser voltado à saúde mental e funcional do empregado.',
        },
        'legal_basis': [{'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943, 'article': 'Art. 458, par. 2, IV — analogia', 'is_primary': True,
            'excerpt': 'Não serão considerados como salário as assistências médica, hospitalar e odontológica prestadas diretamente ou mediante seguro-saúde.'}],
    },
    {
        'name': 'Carro da Empresa para Uso Pessoal',
        'code': 'CAR001',
        'description': 'Concessão de veículo da empresa ao empregado que o utiliza também para fins pessoais. A fração de uso pessoal constitui salário in natura e integra todas as bases de encargos.',
        'category': 'Proventos',
        'esocial_nature_code': '5100',
        'incidence': {
            'inss': True, 'fgts': True, 'irrf': True, 'risk_level': 'high',
            'inss_observation': 'A parcela correspondente ao uso pessoal do veículo integra o salário de contribuição pelo valor de mercado da cessão (Ato Declaratório SRF 3/2000).',
            'irrf_observation': 'O uso pessoal do carro da empresa deve ser incluído mensalmente na base do IRRF pelo valor de mercado do aluguel equivalente.',
            'risk_reason': 'Alto risco: uma das autuações mais frequentes em fiscalização do INSS. Empresas que fornecem carros sem registro e controle de uso pessoal ficam sujeitas a autuação por todo o período de prescrição (5 anos). A valoração do uso pessoal (30% do custo do veículo por mês é prática comum, mas contestável) deve estar documentada em política interna.',
        },
        'legal_basis': [{'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943, 'article': 'Art. 458 c/c Ato Declaratorio SRF 3/2000', 'is_primary': True,
            'excerpt': 'A utilização do veículo de propriedade da empresa para fins particulares do empregado equivale à contraprestação em espécie diversa do dinheiro, tendo natureza salarial.'}],
    },
    {
        'name': 'Celular/Plano Corporativo para Uso Pessoal',
        'code': 'CEL001',
        'description': 'Aparelho celular ou plano de telefonia fornecido pela empresa utilizado parcialmente para fins pessoais. A fração de uso pessoal pode ser configurada como salário in natura.',
        'category': 'Proventos',
        'esocial_nature_code': '5110',
        'incidence': {
            'inss': False, 'fgts': False, 'irrf': False, 'risk_level': 'medium',
            'inss_observation': 'Quando o celular é fornecido como ferramenta de trabalho (para o empregado estar disponível), a RFB e o TST entendem que não há salário in natura. Se o uso pessoal for preponderante, pode ser recaracterizado.',
            'risk_reason': 'Risco médio: a distinção entre ferramenta de trabalho (não salarial) e benefício pessoal (salarial) depende do uso efetivo. Políticas de uso aceitável (Acceptable Use Policy) documentadas reduzem o risco. Celulares de alto valor sob controle do empregado aumentam o risco.',
        },
        'legal_basis': [{'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943, 'article': 'Art. 458, par. 2, I — interpretacao inversa', 'is_primary': True,
            'excerpt': 'Não serão considerados como salário os vestuários, equipamentos e outros acessórios fornecidos ao empregado e utilizados no local de trabalho, para a prestação do serviço.'}],
    },

    # ── Segmento específico ───────────────────────────────────────────────────
    {
        'name': 'Jetons — Participação em Conselho de Administração',
        'code': 'JET001',
        'description': 'Remuneração paga a membros do Conselho de Administração por participação em reuniões, sem vínculo empregatício. Sujeito ao INSS como contribuinte individual e ao IRRF.',
        'category': 'Proventos',
        'esocial_nature_code': '9520',
        'incidence': {
            'inss': True, 'fgts': False, 'irrf': True, 'risk_level': 'medium',
            'inss_observation': 'O conselheiro de administração é segurado obrigatório como contribuinte individual (Art. 12, V, f, Lei 8.212). A empresa retém a contribuição e recolhe a patronal de 20%.',
            'fgts_observation': 'Não há FGTS para membros do Conselho sem vínculo empregatício.',
            'risk_reason': 'Risco médio: a tributação dos jetons é pacífica. O risco está na omissão: empresas que não retêm INSS e IRRF sobre jetons ficam sujeitas a autuação. Membros que acumulam jetons com salário de empregado precisam de tratamento diferenciado.',
        },
        'legal_basis': [{'norm_number': '6.404', 'norm_year': 1976, 'article': 'Art. 152 c/c Lei 8.212/1991 Art. 12', 'is_primary': True,
            'excerpt': 'A assembléia geral fixará o montante global ou individual da remuneração dos administradores, inclusive benefícios de qualquer natureza e verbas de representação.'}],
    },

    # ── Contratos e rescisões específicas ─────────────────────────────────────
    {
        'name': 'Rescisão por Abandono de Emprego',
        'code': 'RND001',
        'description': 'Rescisão por justa causa iniciada pelo empregador em razão do abandono de emprego (ausência injustificada por mais de 30 dias consecutivos). As verbas são as mesmas da justa causa.',
        'category': 'Informativos',
        'esocial_nature_code': '1350',
        'incidence': {
            'inss': False, 'fgts': False, 'irrf': False, 'risk_level': 'high',
            'risk_reason': 'Alto risco: o abandono de emprego exige prova de ausência injustificada (mínimo 30 dias) mais intenção de abandonar (animus abandonandi). O TST exige notificação por AR antes da dispensa por abandono. Sem esses requisitos, a rescisão pode ser convertida em dispensa sem justa causa com todos os reflexos.',
        },
        'legal_basis': [{'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943, 'article': 'Art. 482, i c/c Sumula 32 TST', 'is_primary': True,
            'excerpt': 'Constitui abandono de emprego a falta injustificada ao serviço por mais de 30 dias, bem como a ausência para exercer outro emprego, cabendo ao empregador a prova do ato faltoso do empregado.'}],
    },
    {
        'name': 'Contrato a Prazo Determinado — Verbas na Expiração',
        'code': 'CTD001',
        'description': 'Verbas devidas ao término natural do contrato a prazo determinado: saldo de salário, férias vencidas e proporcionais + 1/3, 13º proporcional e FGTS sem multa de 40%.',
        'category': 'Informativos',
        'esocial_nature_code': '1350',
        'incidence': {
            'inss': False, 'fgts': False, 'irrf': False, 'risk_level': 'low',
            'inss_observation': 'Férias indenizadas e 13º proporcional têm incidências normais (ver rubricas individuais). Este informativo consolida a ausência de multa de 40% na expiração natural.',
            'risk_reason': 'Baixo risco: na expiração natural, não há multa de FGTS nem aviso prévio. O risco está na renovação excessiva — o contrato a prazo que ultrapassa 2 anos ou é renovado mais de uma vez se converte em prazo indeterminado, tornando a rescisão seguinte em dispensa sem justa causa.',
        },
        'legal_basis': [{'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943, 'article': 'Art. 445 e 451', 'is_primary': True,
            'excerpt': 'O contrato de trabalho por prazo determinado não poderá ser estipulado por mais de dois anos. Não poderá ser prorrogado mais de uma vez, tornando-se, em caso de nova prorrogação, em contrato de prazo indeterminado.'}],
    },

    # ── Gratificação convencional ──────────────────────────────────────────────
    {
        'name': 'Décimo Quarto Salário (Norma Coletiva)',
        'code': 'G14S1',
        'description': 'Gratificação equivalente a um salário adicional por ano, paga em data prevista em norma coletiva. Tem natureza salarial e integra todos os encargos.',
        'category': 'Proventos',
        'esocial_nature_code': '1100',
        'incidence': {
            'inss': True, 'fgts': True, 'irrf': True, 'risk_level': 'medium',
            'inss_observation': 'Por ser verba habitual de natureza salarial, integra o salário de contribuição e o FGTS integralmente.',
            'irrf_observation': 'Tributado pelo IRRF no mês do pagamento. O 14º salário pode ser incorporado ao cálculo das médias para férias, 13º e aviso prévio se pago com habitualidade.',
            'risk_reason': 'Risco médio: empresas que pagam o 14º de forma unilateral, sem norma coletiva, e depois tentam suprimir, incorrem em supressão de vantagem habitual (Art. 468 CLT). A norma coletiva que o prevê deve ser renovada anualmente para não consolidar o direito.',
        },
        'legal_basis': [{'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943, 'article': 'Art. 457 c/c Art. 611 c/c Sumula 203 TST', 'is_primary': True,
            'excerpt': 'As gratificações ajustadas pela convenção ou acordo coletivo têm natureza salarial e integram a remuneração para todos os fins de direito.'}],
    },
]


class Command(BaseCommand):
    help = 'Seed v1.4 — adiciona 25 rubricas (retenções na fonte, rural, construção civil, cooperativas, modernos, contratos específicos)'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        from apps.catalog.models import Category, EsocialNature, Rubric
        from apps.legislation.models import LegalNorm, LegalBasis
        from apps.engine.models import Incidence

        self.stdout.write('Criando naturezas eSocial v1.4...')
        for data in V14_NATURES:
            EsocialNature.objects.get_or_create(
                code=data['code'],
                defaults={
                    'description': data['description'],
                    'is_salary_nature': data['is_salary_nature'],
                }
            )

        self.stdout.write('Criando normas legais v1.4...')
        norm_map = {}
        for norm in LegalNorm.objects.all():
            norm_map[(norm.number, norm.year)] = norm

        for data in V14_NORMS:
            norm, _ = LegalNorm.objects.get_or_create(
                number=data['number'],
                year=data['year'],
                defaults=data
            )
            norm_map[(data['number'], data['year'])] = norm

        self.stdout.write('Criando rubricas v1.4...')
        created_count = 0
        for r in RUBRICAS_V14:
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
