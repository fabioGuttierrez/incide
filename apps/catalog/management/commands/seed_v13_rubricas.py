"""
Seed v1.3 — 30 rubricas cobrindo:
  - Encargos patronais informativos (INSS Patronal, Sistema S, Salário Educação, FGTS/13)
  - Jornada avançada (escala 12x36, prontidão, trabalho em domingo, HE noturna)
  - Rescisório avançado (Art. 479, Art. 480, justa causa, PDV, comissões médias)
  - Indenizações judiciais (danos morais, acidente, lucros cessantes)
  - Benefícios INSS avançados (auxílio-acidente, abono PIS/PASEP)
  - Trabalho intermitente (remuneração, 13º, férias proporcionais)
  - Contribuições sindicais e associativas
  - Doméstico completo (13º, férias, aviso prévio, FGTS/DAE)
  - Descontos especiais (alimentação PAT, plano de saúde)
  - Teletrabalho — ressarcimento de despesas

Execute com: python manage.py seed_v13_rubricas
"""
from django.core.management.base import BaseCommand
from django.db import transaction


V13_NATURES = [
    {'code': '1082', 'description': 'Prontidao (Art. 244, par. 3, CLT)', 'is_salary_nature': True},
    {'code': '1700', 'description': 'Trabalho Intermitente — Remuneracao por Periodo', 'is_salary_nature': True},
    {'code': '1710', 'description': 'Trabalho Intermitente — 13 Salario Proporcional', 'is_salary_nature': True},
    {'code': '1720', 'description': 'Trabalho Intermitente — Ferias Proporcionais', 'is_salary_nature': False},
    {'code': '1621', 'description': 'Domestico — 13 Salario', 'is_salary_nature': True},
    {'code': '1622', 'description': 'Domestico — Ferias + 1/3', 'is_salary_nature': False},
    {'code': '1623', 'description': 'Domestico — Aviso Previo Indenizado', 'is_salary_nature': False},
    {'code': '1624', 'description': 'Domestico — FGTS via DAE (Informativo)', 'is_salary_nature': False},
    {'code': '9181', 'description': 'Contribuicao Assistencial Sindical (Facultativa)', 'is_salary_nature': False},
    {'code': '9182', 'description': 'Taxa Confederativa / Negocial (Facultativa)', 'is_salary_nature': False},
    {'code': '9800', 'description': 'Contribuicao Sistema S / Terceiros (Patronal)', 'is_salary_nature': False},
    {'code': '9810', 'description': 'Salario Educacao 2,5% (Encargo Patronal)', 'is_salary_nature': False},
    {'code': '9900', 'description': 'INSS Patronal 20% (Encargo Empresa)', 'is_salary_nature': False},
    {'code': '9950', 'description': 'Abono PIS/PASEP (Informativo)', 'is_salary_nature': False},
]

V13_NORMS = [
    {
        'norm_type': 'lei', 'number': '9.601', 'year': 1998,
        'title': 'Lei 9.601/1998 — Contratos a Prazo e Trabalho Temporario',
        'official_link': 'https://www.planalto.gov.br/ccivil_03/leis/l9601.htm',
    },
    {
        'norm_type': 'lei', 'number': '7.998', 'year': 1990,
        'title': 'Lei 7.998/1990 — Programa Seguro-Desemprego e Abono Salarial PIS',
        'official_link': 'https://www.planalto.gov.br/ccivil_03/leis/l7998.htm',
    },
    {
        'norm_type': 'lei', 'number': '9.012', 'year': 1995,
        'title': 'Lei 9.012/1995 — Salario Educacao',
        'official_link': 'https://www.planalto.gov.br/ccivil_03/leis/l9012.htm',
    },
]

RUBRICAS_V13 = [

    # ── Encargos patronais informativos ───────────────────────────────────────
    {
        'name': 'INSS Patronal 20%',
        'code': 'INP001',
        'description': 'Contribuição previdenciária patronal de 20% sobre o total das remunerações pagas aos empregados, exceto para empresas aderentes ao Simples Nacional ou ao CPRB.',
        'category': 'Bases de Cálculo',
        'esocial_nature_code': '9900',
        'incidence': {
            'inss': False, 'fgts': False, 'irrf': False, 'risk_level': 'medium',
            'inss_observation': 'Encargo patronal — não é desconto do empregado. Empresas optantes pelo Simples Nacional ou pelo CPRB (desoneração da folha) possuem alíquotas e bases diferenciadas.',
            'risk_reason': 'Risco médio: empresas na desoneração da folha (CPRB variable %) precisam atenção especial. A base 20% incide inclusive sobre pró-labore, gorjetas e gratificações — erros na base geram diferença expressiva de GPS.',
        },
        'legal_basis': [{'norm_number': '8.212', 'norm_year': 1991, 'article': 'Art. 22, I', 'is_primary': True,
            'excerpt': 'A contribuição a cargo da empresa, destinada à Seguridade Social, é de 20% sobre o total das remunerações pagas, devidas ou creditadas a qualquer título, durante o mês, aos segurados empregados e trabalhadores avulsos.'}],
    },
    {
        'name': 'Contribuição Sistema S / Terceiros',
        'code': 'SIS001',
        'description': 'Contribuições destinadas ao SESI/SESC, SENAI/SENAC, SEBRAE, INCRA e FNDE, calculadas sobre a folha de salários. Alíquotas variam por CNAE (0,2% a 5,8%).',
        'category': 'Bases de Cálculo',
        'esocial_nature_code': '9800',
        'incidence': {
            'inss': False, 'fgts': False, 'irrf': False, 'risk_level': 'medium',
            'inss_observation': 'Encargo patronal. Alíquota total varia de acordo com o CNAE principal da empresa. Simples Nacional está isento de parte dessas contribuições.',
            'risk_reason': 'Risco médio: alíquota errada por CNAE incorreto é causa frequente de autuação. A mudança de atividade principal deve refletir imediatamente no CNAE e nas alíquotas dos terceiros.',
        },
        'legal_basis': [{'norm_number': '8.212', 'norm_year': 1991, 'article': 'Art. 22, I c/c Lei 2.613/1955', 'is_primary': True,
            'excerpt': 'São contribuições das empresas as devidas às entidades privadas de serviço social e de formação profissional vinculadas ao sistema sindical, distribuídas conforme decreto regulamentador.'}],
    },
    {
        'name': 'Salário Educação (2,5%)',
        'code': 'SAE001',
        'description': 'Contribuição social patronal de 2,5% sobre o total das remunerações pagas, destinada ao financiamento do ensino fundamental público (FNDE).',
        'category': 'Bases de Cálculo',
        'esocial_nature_code': '9810',
        'incidence': {
            'inss': False, 'fgts': False, 'irrf': False, 'risk_level': 'low',
            'inss_observation': 'Encargo patronal — recolhido junto com as demais contribuições previdenciárias. Simples Nacional pode ser isento dependendo da fase.',
            'risk_reason': 'Baixo risco: alíquota fixa de 2,5%. Atenção para empresas no Simples Nacional, que podem estar isentas.',
        },
        'legal_basis': [{'norm_number': '9.012', 'norm_year': 1995, 'article': 'Art. 1', 'is_primary': True,
            'excerpt': 'O salário-educação, previsto no art. 212, § 5°, da Constituição Federal, é calculado com base na alíquota de contribuição de 2,5% sobre o total de remunerações pagas ou creditadas pelas empresas a qualquer título ao segurados empregados.'}],
    },
    {
        'name': 'FGTS sobre 13º Salário (Encargo Patronal)',
        'code': 'FG131',
        'description': 'Depósito de FGTS de 8% sobre o 13º salário, realizado pela empresa em duas etapas: na 1ª parcela (novembro) e na rescisão ou dezembro.',
        'category': 'Bases de Cálculo',
        'esocial_nature_code': '9110',
        'incidence': {
            'inss': False, 'fgts': False, 'irrf': False, 'risk_level': 'low',
            'fgts_observation': 'O depósito do FGTS sobre 13º é obrigação patronal distinta do FGTS mensal. Deve ser recolhido até o dia 20/12 (parcela de dezembro) e na rescisão (proporcional).',
            'risk_reason': 'Baixo risco quanto à incidência. O risco está na omissão do depósito, especialmente no 13º rescisório, quando é comum a empresa esquecer de recolher o FGTS proporcional.',
        },
        'legal_basis': [{'norm_number': '8.036', 'norm_year': 1990, 'article': 'Art. 15, par. 6', 'is_primary': True,
            'excerpt': 'Entende-se por rescisão do contrato de trabalho, para fins desta Lei, a cessação do vínculo empregatício entre o trabalhador e o empregador, por qualquer das causas previstas na legislação trabalhista, ensejando o saque dos depósitos existentes na conta vinculada.'}],
    },

    # ── Jornada avançada ──────────────────────────────────────────────────────
    {
        'name': 'Hora Extra — Escala 12x36',
        'code': 'HE12X1',
        'description': 'Horas excedentes à jornada de 12h na escala 12x36, quando não compensadas pelo intervalo de 36h ou quando a escala não está prevista em norma coletiva.',
        'category': 'Proventos',
        'esocial_nature_code': '1040',
        'incidence': {
            'inss': True, 'fgts': True, 'irrf': True, 'risk_level': 'medium',
            'inss_observation': 'Integra o salário de contribuição por ser hora extra com natureza salarial.',
            'risk_reason': 'Risco médio: após a Reforma Trabalhista (Art. 59-A CLT), a escala 12x36 pode ser formalizada por norma coletiva ou acordo individual. Sem formalização adequada, todas as horas da 9ª em diante são extras. Compensação automática do repouso é válida, mas horas adicionais mantêm encargos.',
        },
        'legal_basis': [{'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943, 'article': 'Art. 59-A c/c Sumula 444 TST', 'is_primary': True,
            'excerpt': 'É válida, em caráter excepcional, a jornada de doze horas de trabalho por trinta e seis de descanso, prevista em lei ou ajustada exclusivamente mediante acordo coletivo de trabalho ou convenção coletiva de trabalho.'}],
    },
    {
        'name': 'Prontidão (Art. 244, §3º CLT)',
        'code': 'PRT001',
        'description': 'Período em que o empregado ferroviário (e por analogia outros setores) aguarda chamado para serviço sem prestar atividade, remunerado a 1/3 da hora normal.',
        'category': 'Proventos',
        'esocial_nature_code': '1082',
        'incidence': {
            'inss': True, 'fgts': True, 'irrf': True, 'risk_level': 'low',
            'inss_observation': 'Apesar do valor reduzido (1/3), integra o salário de contribuição por ser verba de natureza salarial paga pelo tempo à disposição.',
            'risk_reason': 'Baixo risco: regra expressa no Art. 244 §3 CLT. Atenção para equiparação com o sobreaviso (cuja jurisprudência é distinta quanto ao pagamento de 1/3 versus 1/3 proporcional).',
        },
        'legal_basis': [{'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943, 'article': 'Art. 244, par. 3', 'is_primary': True,
            'excerpt': 'Considera-se de prontidão o empregado que ficar nas dependências da estrada, aguardando ordens, sendo remunerado por esse período com 1/3 (um terço) do salário da hora normal.'}],
    },
    {
        'name': 'Trabalho em Domingo Não Compensado',
        'code': 'TDB001',
        'description': 'Remuneração adicional pelo trabalho realizado em domingos sem a correspondente folga compensatória na semana, com acréscimo de 100%.',
        'category': 'Proventos',
        'esocial_nature_code': '1010',
        'incidence': {
            'inss': True, 'fgts': True, 'irrf': True, 'risk_level': 'medium',
            'inss_observation': 'O adicional pelo trabalho em domingo não compensado tem natureza salarial e integra a base de cálculo de todos os encargos.',
            'risk_reason': 'Risco médio: empresas que escalam empregados aos domingos sem garantir a compensação ficam sujeitas ao pagamento em dobro + reflexos no 13º e férias. A prova de que a compensação ocorreu na mesma semana é essencial.',
        },
        'legal_basis': [{'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943, 'article': 'Art. 67 c/c Sumula 461 TST', 'is_primary': True,
            'excerpt': 'Será assegurado a todo empregado um descanso semanal de 24 horas consecutivas, o qual, salvo motivo de conveniência pública ou necessidade imperiosa do serviço, deverá coincidir com o domingo.'}],
    },
    {
        'name': 'Hora Extra Noturna Cumulativa',
        'code': 'HEN001',
        'description': 'Hora extra trabalhada no período noturno (22h às 5h), acumulando o adicional de horas extras (50% ou mais) com o adicional noturno (20%), calculados sobre a hora ficta noturna.',
        'category': 'Proventos',
        'esocial_nature_code': '1040',
        'incidence': {
            'inss': True, 'fgts': True, 'irrf': True, 'risk_level': 'medium',
            'inss_observation': 'A cumulatividade dos adicionais é pacífica no TST — a hora extra noturna integra plenamente o salário de contribuição.',
            'risk_reason': 'Risco médio: o cálculo sobre a hora ficta noturna (52m30s) é frequentemente negligenciado. Empresas que calculam a HE noturna sobre 60 minutos ao invés da hora ficta pagam a menos e geram passivo trabalhista.',
        },
        'legal_basis': [{'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943, 'article': 'Art. 73 c/c Sumula 60 TST', 'is_primary': True,
            'excerpt': 'O trabalho noturno terá remuneração superior à do diurno e, para esse efeito, sua remuneração terá um acréscimo de 20% pelo menos sobre a hora diurna. A hora noturna corresponde a 52 minutos e 30 segundos.'}],
    },

    # ── Rescisório avançado ───────────────────────────────────────────────────
    {
        'name': 'Indenização Art. 479 CLT — Rescisão Antecipada pelo Empregador',
        'code': 'RI479',
        'description': 'Indenização devida ao empregado quando o empregador rescinde antecipadamente contrato de trabalho por prazo determinado, equivalente à metade dos salários restantes.',
        'category': 'Informativos',
        'esocial_nature_code': '1350',
        'incidence': {
            'inss': False, 'fgts': False, 'irrf': False, 'risk_level': 'low',
            'inss_observation': 'Natureza indenizatória — não integra o salário de contribuição nem a base do FGTS.',
            'irrf_observation': 'Conforme RIR/2018, Art. 39: indenizações por rescisão do contrato de trabalho são isentas do IRRF.',
            'risk_reason': 'Baixo risco de encargos. O risco está na própria situação: rescisão antecipada de contrato a prazo sem cláusula liberatória gera obrigação automática da indenização, ignorada por muitas empresas.',
        },
        'legal_basis': [{'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943, 'article': 'Art. 479', 'is_primary': True,
            'excerpt': 'Nos contratos que tenham termo estipulado, o empregador que, sem justa causa, despedir o empregado será obrigado a pagar-lhe, a título de indenização, e por metade, a remuneração a que teria direito até o termo do contrato.'}],
    },
    {
        'name': 'Desconto Art. 480 CLT — Rescisão Antecipada pelo Empregado',
        'code': 'DP480',
        'description': 'Desconto aplicado ao empregado que pede demissão antes do término de contrato por prazo determinado, equivalente ao prejuízo causado ao empregador (limitado a 1 mês de salário).',
        'category': 'Descontos',
        'esocial_nature_code': '1350',
        'incidence': {
            'inss': False, 'fgts': False, 'irrf': False, 'risk_level': 'low',
            'risk_reason': 'Baixo risco: desconto líquido do salário final. Atenção para o limite máximo de 1 mês de salário. Empresas raramente formalizam esse desconto, mas têm direito.',
        },
        'legal_basis': [{'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943, 'article': 'Art. 480', 'is_primary': True,
            'excerpt': 'Havendo termo estipulado, o empregado não se poderá desligar do contrato, sem justa causa, sob pena de ser obrigado a indenizar o empregador dos prejuízos que desse fato lhe resultarem.'}],
    },
    {
        'name': 'Rescisão com Justa Causa — Verbas Remanescentes',
        'code': 'VRJ001',
        'description': 'Verbas devidas ao empregado dispensado por justa causa: saldo de salário e férias vencidas + 1/3. Não há aviso prévio, 13º proporcional nem multa do FGTS.',
        'category': 'Informativos',
        'esocial_nature_code': '1350',
        'incidence': {
            'inss': False, 'fgts': False, 'irrf': False, 'risk_level': 'high',
            'inss_observation': 'As férias vencidas têm natureza indenizatória — não integram a base de contribuição. O saldo de salário integra normalmente.',
            'irrf_observation': 'Férias vencidas + 1/3 recebidos na rescisão são isentos de IRRF (RIR/2018, Art. 39).',
            'risk_reason': 'Alto risco: enquadrar dispensa como justa causa sem provas suficientes é nulo ou convertido em dispensa sem justa causa pelo TST, gerando reversão total das verbas e multas. A documentação do fato ensejador é essencial.',
        },
        'legal_basis': [{'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943, 'article': 'Art. 482 c/c Art. 146', 'is_primary': True,
            'excerpt': 'Constituem justa causa para rescisão do contrato de trabalho pelo empregador: a) ato de improbidade; b) incontinência de conduta ou mau procedimento; c) negociação habitual por conta própria ou alheia sem permissão do empregador...'}],
    },
    {
        'name': 'Comissões Médias Rescisórias',
        'code': 'CMR001',
        'description': 'Média das comissões recebidas nos últimos 12 meses, integrada às verbas rescisórias: aviso prévio, 13º rescisório e férias proporcionais.',
        'category': 'Bases de Cálculo',
        'esocial_nature_code': '1110',
        'incidence': {
            'inss': True, 'fgts': True, 'irrf': True, 'risk_level': 'medium',
            'inss_observation': 'As comissões integram o salário de contribuição em todas as verbas rescisórias por serem verba de natureza salarial.',
            'risk_reason': 'Risco médio: a integração das comissões médias nas verbas rescisórias é ignorada por muitos empregadores. A média deve incluir os meses com comissão variável, e o cálculo incorreto gera diferença significativa no acerto.',
        },
        'legal_basis': [{'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943, 'article': 'Art. 457 c/c Art. 487, par. 1', 'is_primary': True,
            'excerpt': 'O salário do empregado que tiver parte variável será calculado, para os efeitos do aviso prévio, sobre a média percebida nos últimos doze meses de serviço.'}],
    },
    {
        'name': 'PDV — Plano de Demissão Voluntária',
        'code': 'PDE001',
        'description': 'Indenização paga ao empregado que adere voluntariamente ao PDV. Pode ser isenta de IR e INSS quando configurada como rescisão por mútuo acordo ou indenização especial.',
        'category': 'Informativos',
        'esocial_nature_code': '1350',
        'incidence': {
            'inss': False, 'fgts': False, 'irrf': False, 'risk_level': 'high',
            'inss_observation': 'O parcela indenizatória do PDV (valor acima das verbas legais) não integra o salário de contribuição, conforme posição consolidada do TST.',
            'irrf_observation': 'O STF (ADI 1.231) reconheceu a isenção do IR sobre PDV pago por entidade governamental. Para o setor privado, o STJ segue a mesma tese. Recomenda-se guarda do plano e comprovação do caráter indenizatório.',
            'risk_reason': 'Alto risco: a linha entre PDV (indenizatório, isento) e bonificação pela saída (tributável) é tênue. PDVs mal estruturados são autuados pela RFB como rendimento do trabalho. É essencial ter o plano formalizado com condições claras e abrangência coletiva.',
        },
        'legal_basis': [{'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943, 'article': 'Art. 484-A c/c ADI 1.231 STF', 'is_primary': True,
            'excerpt': 'O contrato de trabalho pode ser extinto por acordo entre empregado e empregador, caso em que serão devidas as seguintes verbas trabalhistas.'}],
    },

    # ── Indenizações judiciais ─────────────────────────────────────────────────
    {
        'name': 'Indenização por Danos Morais — Judicial',
        'code': 'IDM001',
        'description': 'Valor pago por força de sentença ou acordo judicial a título de danos morais decorrentes da relação de trabalho. Não integra o conceito de rendimento do trabalho.',
        'category': 'Informativos',
        'esocial_nature_code': '1350',
        'incidence': {
            'inss': False, 'fgts': False, 'irrf': False, 'risk_level': 'low',
            'inss_observation': 'Natureza indenizatória — não integra o salário de contribuição (RE 1.072.220 STF, 2021).',
            'irrf_observation': 'Não incide IRRF sobre danos morais, conforme RE 1.072.220 STF (Tema 808). Empresas que retinham IR na fonte deverão restituir os valores.',
            'risk_reason': 'Baixo risco de encargos após o RE 1.072.220 STF (2021) que fixou a isenção. Atenção: danos materiais (lucros cessantes) têm tratamento diferente e podem estar sujeitos ao IRRF.',
        },
        'legal_basis': [{'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943, 'article': 'RE 1.072.220 STF — Tema 808', 'is_primary': True,
            'excerpt': 'Não incide imposto de renda sobre os valores pagos a título de indenização por danos morais, independentemente da natureza da relação jurídica estabelecida entre as partes (pública ou privada).'}],
    },
    {
        'name': 'Indenização por Acidente de Trabalho — Judicial',
        'code': 'IAT001',
        'description': 'Indenização judicial por danos materiais e morais decorrentes de acidente ou doença do trabalho, incluindo lucros cessantes e dano estético.',
        'category': 'Informativos',
        'esocial_nature_code': '1350',
        'incidence': {
            'inss': False, 'fgts': False, 'irrf': False, 'risk_level': 'high',
            'inss_observation': 'Natureza indenizatória — não integra o salário de contribuição.',
            'irrf_observation': 'A parcela de danos morais é isenta (RE 1.072.220). A parcela de lucros cessantes pode ser tributável — consultar advogado trabalhista para segregar as parcelas na sentença.',
            'risk_reason': 'Alto risco reputacional e financeiro: indenizações por acidente costumam ser de grande valor e incluir pensão vitalícia. Empresas sem programa de saúde e segurança (PCMSO, PPRA) ficam mais expostas. A segregação entre dano moral e material na sentença é fundamental para determinar a tributação.',
        },
        'legal_basis': [{'norm_number': '8.213', 'norm_year': 1991, 'article': 'Art. 120 e 121 c/c Codigo Civil Art. 932', 'is_primary': True,
            'excerpt': 'Nos casos de negligência quanto às normas de saúde e segurança do trabalho indicadas para a proteção individual e coletiva, a Previdência Social proporá ação regressiva contra os responsáveis.'}],
    },
    {
        'name': 'Indenização por Lucros Cessantes — Judicial',
        'code': 'ILU001',
        'description': 'Parcela de indenização judicial correspondente à perda de renda futura do trabalhador acidentado. Sujeita ao IRRF por ter natureza de rendimento substituído.',
        'category': 'Informativos',
        'esocial_nature_code': '1350',
        'incidence': {
            'inss': False, 'fgts': False, 'irrf': True, 'risk_level': 'high',
            'irrf_observation': 'Diferentemente dos danos morais (isentos), os lucros cessantes são tributáveis pelo IRRF por representarem substituição de renda do trabalho (Decreto 9.580/2018, Art. 36).',
            'risk_reason': 'Alto risco: a segregação entre dano moral (isento) e lucros cessantes (tributável) na sentença ou acordo é frequentemente omitida, levando a tributação incorreta. Retenção inadequada gera autuação pela RFB tanto por excesso quanto por falta.',
        },
        'legal_basis': [{'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943, 'article': 'RE 1.072.220 STF e Decreto 9.580/2018 Art. 36', 'is_primary': True,
            'excerpt': 'São tributáveis pelo imposto de renda os rendimentos que representem substituição de rendimentos do trabalho, não enquadrados nas isenções do art. 39 do Decreto 9.580/2018.'}],
    },

    # ── Benefícios INSS avançados ──────────────────────────────────────────────
    {
        'name': 'Auxílio-Acidente INSS (30%) — Art. 86 Lei 8.213',
        'code': 'AAI001',
        'description': 'Benefício permanente de 30% do salário de benefício, pago pelo INSS ao segurado que, após alta da doença acidentária, apresenta redução da capacidade laboral.',
        'category': 'Informativos',
        'esocial_nature_code': '1420',
        'incidence': {
            'inss': False, 'fgts': False, 'irrf': False, 'risk_level': 'medium',
            'inss_observation': 'O auxílio-acidente é pago pelo INSS (não pela empresa). A empresa continua pagando o salário normal ao empregado — o benefício é acumulável com o salário.',
            'fgts_observation': 'O FGTS é depositado normalmente sobre o salário pago pela empresa. O auxílio-acidente em si não é base de FGTS.',
            'risk_reason': 'Risco médio: a empresa deve registrar corretamente o CAT (Comunicação de Acidente de Trabalho) para garantir que o INSS reconheça o vínculo acidentário. A falta do CAT pode levar o INSS a negar o benefício, voltando o ônus para a empresa.',
        },
        'legal_basis': [{'norm_number': '8.213', 'norm_year': 1991, 'article': 'Art. 86', 'is_primary': True,
            'excerpt': 'O auxílio-acidente será concedido, como indenização, ao segurado quando, após consolidação das lesões decorrentes de acidente de qualquer natureza, resultarem sequelas que impliquem redução da capacidade para o trabalho que habitualmente exercia.'}],
    },
    {
        'name': 'Abono PIS/PASEP',
        'code': 'ABO001',
        'description': 'Abono salarial anual de até 1 salário mínimo, pago aos trabalhadores com vínculo formal há pelo menos 12 meses e rendimento médio de até 2 SM. Banco do Brasil e Caixa pagam diretamente.',
        'category': 'Informativos',
        'esocial_nature_code': '9950',
        'incidence': {
            'inss': False, 'fgts': False, 'irrf': False, 'risk_level': 'low',
            'inss_observation': 'Pago pelo Fundo PIS/PASEP — não é encargo da empresa. A empresa deve apenas manter as informações corretas na RAIS/eSocial para que o trabalhador receba o benefício.',
            'risk_reason': 'Baixo risco de encargos. O risco está no cadastro incorreto na RAIS: trabalhadores com informações erradas não recebem o abono e podem responsabilizar a empresa. Manter RAIS e eSocial atualizados é essencial.',
        },
        'legal_basis': [{'norm_number': '7.998', 'norm_year': 1990, 'article': 'Art. 9', 'is_primary': True,
            'excerpt': 'Fica instituído o Abono Salarial anual, no valor de 1 (um) salário mínimo, ao trabalhador que preencher os requisitos de: (I) estar cadastrado há pelo menos 5 anos no PIS/PASEP; (II) ter trabalhado com carteira assinada por pelo menos 30 dias no ano base; (III) ter recebido remuneração mensal média de até 2 salários mínimos durante o período trabalhado.'}],
    },

    # ── Trabalho intermitente ─────────────────────────────────────────────────
    {
        'name': 'Trabalho Intermitente — Remuneração',
        'code': 'TIN001',
        'description': 'Remuneração proporcional do trabalhador intermitente pelo período efetivamente trabalhado, não menor que a hora do salário mínimo ou do piso convencional.',
        'category': 'Proventos',
        'esocial_nature_code': '1700',
        'incidence': {
            'inss': True, 'fgts': True, 'irrf': True, 'risk_level': 'medium',
            'inss_observation': 'Incide INSS normal sobre a remuneração proporcional. O empregador deve recolher em cada convocação paga.',
            'fgts_observation': 'O FGTS (8%) é depositado sobre cada pagamento feito ao trabalhador intermitente.',
            'irrf_observation': 'O IRRF é calculado sobre a remuneração acumulada do mês, conforme tabela progressiva.',
            'risk_reason': 'Risco médio: o contrato intermitente deve ser escrito e conter valor da hora. O empregador que não convoca o trabalhador por 12 meses pode ter o contrato rescindido por ausência de convocação. A falta de formalidade na convocação pode ser considerada vínculo empregatício clássico.',
        },
        'legal_basis': [{'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943, 'article': 'Art. 452-A', 'is_primary': True,
            'excerpt': 'O contrato de trabalho intermitente deve ser celebrado por escrito e deve conter especificamente o valor da hora de trabalho, que não pode ser inferior ao valor horário do salário mínimo ou àquele devido aos demais empregados do estabelecimento que exerçam a mesma função.'}],
    },
    {
        'name': 'Trabalho Intermitente — 13º Salário Proporcional',
        'code': 'TI13S',
        'description': 'Décimo terceiro salário proporcional pago ao trabalhador intermitente ao final de cada período de convocação ou quando solicitado.',
        'category': 'Proventos',
        'esocial_nature_code': '1710',
        'incidence': {
            'inss': True, 'fgts': False, 'irrf': True, 'risk_level': 'medium',
            'inss_observation': 'O 13º proporcional integra o salário de contribuição do trabalhador intermitente.',
            'fgts_observation': 'O FGTS sobre o 13º do intermitente segue a regra geral, recolhido na competência de pagamento.',
            'risk_reason': 'Risco médio: o trabalhador intermitente tem direito ao 13º, férias + 1/3 e previdência em cada pagamento — pagamento por fora sem FGTS e INSS gera passivo significativo.',
        },
        'legal_basis': [{'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943, 'article': 'Art. 452-A, par. 6, I', 'is_primary': True,
            'excerpt': 'Ao final de cada período de prestação de serviço, o empregado receberá o pagamento imediato das seguintes parcelas: I — remuneração; II — férias proporcionais com acréscimo de um terço; III — décimo terceiro salário proporcional.'}],
    },
    {
        'name': 'Trabalho Intermitente — Férias Proporcionais',
        'code': 'TIF001',
        'description': 'Férias proporcionais + 1/3 pagas ao trabalhador intermitente ao final de cada convocação, incluídas no recibo de pagamento.',
        'category': 'Proventos',
        'esocial_nature_code': '1720',
        'incidence': {
            'inss': False, 'fgts': False, 'irrf': True, 'risk_level': 'medium',
            'inss_observation': 'As férias proporcionais pagas ao intermitente têm natureza indenizatória, não integrando o salário de contribuição.',
            'irrf_observation': 'As férias proporcionais do intermitente são tributáveis pelo IRRF, conforme tabela progressiva.',
            'risk_reason': 'Risco médio: mesmo com a natureza indenizatória das férias, o IRRF deve ser retido. Empresas que não incluem os adicionais de férias no pagamento do intermitente ficam expostas a reclamações trabalhistas.',
        },
        'legal_basis': [{'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943, 'article': 'Art. 452-A, par. 6, II', 'is_primary': True,
            'excerpt': 'Ao final de cada período de prestação de serviço, o empregado receberá o pagamento imediato das seguintes parcelas: II — férias proporcionais com acréscimo de um terço.'}],
    },

    # ── Contribuições sindicais e associativas ─────────────────────────────────
    {
        'name': 'Contribuição Assistencial Sindical (Facultativa)',
        'code': 'CAS001',
        'description': 'Desconto cobrado pelo sindicato da categoria, previsto em norma coletiva, para custeio das atividades assistenciais. Após a Reforma de 2017, só é válida com autorização expressa e individual do empregado.',
        'category': 'Descontos',
        'esocial_nature_code': '9181',
        'incidence': {
            'inss': False, 'fgts': False, 'irrf': False, 'risk_level': 'high',
            'risk_reason': 'Alto risco: após a Reforma Trabalhista (2017), o STF firmou entendimento (ADI 5794) que a contribuição assistencial depende de autorização expressa e individual do empregado. Descontar sem autorização gera responsabilidade trabalhista e possibilidade de devolução em dobro (Art. 940 CC). Verificar se o empregado assinou autorização antes de descontar.',
        },
        'legal_basis': [{'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943, 'article': 'Art. 462 c/c ADI 5794 STF', 'is_primary': True,
            'excerpt': 'Ao empregador é vedado efetuar qualquer desconto nos salários do empregado, salvo quando este resultar de adiantamentos, de dispositivos de lei ou de contrato coletivo. O STF declarou que a contribuição assistencial exige autorização individual.'}],
    },
    {
        'name': 'Taxa Confederativa / Negocial',
        'code': 'TCN001',
        'description': 'Contribuição prevista em norma coletiva para custeio do sistema confederativo ou das negociações. Também exige autorização individual do empregado após a Reforma Trabalhista.',
        'category': 'Descontos',
        'esocial_nature_code': '9182',
        'incidence': {
            'inss': False, 'fgts': False, 'irrf': False, 'risk_level': 'high',
            'risk_reason': 'Alto risco: o STF (RE 198.093) declarou a inconstitucionalidade da cobrança compulsória da taxa confederativa de não associados. Após ADI 5794 (2018), toda contribuição sindical de natureza negocial exige autorização individual. Verificar associação e autorização assinada antes do desconto.',
        },
        'legal_basis': [{'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943, 'article': 'Art. 8, IV CF/88 c/c RE 198.093 STF', 'is_primary': True,
            'excerpt': 'A assembleia geral fixará a contribuição que, em se tratando de categoria profissional, será descontada em folha, para custeio do sistema confederativo da representação sindical respectiva, independentemente da contribuição prevista em lei.'}],
    },

    # ── Doméstico completo ────────────────────────────────────────────────────
    {
        'name': 'Doméstico — 13º Salário',
        'code': 'D13D01',
        'description': '13º salário do empregado doméstico, pago até 30/11 (1ª parcela) e 20/12 (2ª parcela). FGTS deve ser recolhido via DAE (Documento de Arrecadação do eSocial).',
        'category': 'Proventos',
        'esocial_nature_code': '1621',
        'incidence': {
            'inss': True, 'fgts': True, 'irrf': True, 'risk_level': 'low',
            'inss_observation': 'O INSS do doméstico sobre o 13º é recolhido via DAE juntamente com o FGTS, com alíquota patronal de 8% + 0,8% (RAT).',
            'fgts_observation': 'O FGTS do doméstico é recolhido via DAE — documento específico do eSocial. Não use FGTS normal (GFIP). A alíquota é 8% sobre o 13º.',
            'risk_reason': 'Baixo risco de incidência — o risco está no veículo de recolhimento: domésticos exigem DAE, não GFIP/DARF comum. Erros no recolhimento (veículo errado) podem gerar multas do eSocial.',
        },
        'legal_basis': [{'norm_number': '150', 'norm_year': 2015, 'article': 'Art. 22 c/c Art. 23', 'is_primary': True,
            'excerpt': 'São devidos ao empregado doméstico os seguintes direitos: XIII — décimo terceiro salário com base na remuneração integral ou no valor da aposentadoria.'}],
    },
    {
        'name': 'Doméstico — Férias + 1/3',
        'code': 'DFE001',
        'description': 'Férias gozadas e respectivo adicional de 1/3 do empregado doméstico, nos mesmos termos do CLT. FGTS via DAE. LC 150/2015.',
        'category': 'Proventos',
        'esocial_nature_code': '1622',
        'incidence': {
            'inss': False, 'fgts': False, 'irrf': True, 'risk_level': 'low',
            'fgts_observation': 'O FGTS sobre férias do doméstico segue a regra geral (não incide sobre as férias propriamente ditas), mas incide sobre a remuneração do período de férias. Recolhimento via DAE.',
            'irrf_observation': 'O adicional de 1/3 é isento do IRRF. A remuneração das férias é tributável.',
            'risk_reason': 'Baixo risco de incidência. Atenção ao veículo de recolhimento (DAE) e à extinção do benefício de isenção do INSS nas férias domésticas para fins de cálculo.',
        },
        'legal_basis': [{'norm_number': '150', 'norm_year': 2015, 'article': 'Art. 17 a 22', 'is_primary': True,
            'excerpt': 'O empregado doméstico terá direito a férias anuais remuneradas de trinta dias com acréscimo de pelo menos um terço do salário normal.'}],
    },
    {
        'name': 'Doméstico — Aviso Prévio Indenizado',
        'code': 'DAV001',
        'description': 'Aviso prévio indenizado do empregado doméstico na dispensa sem justa causa, calculado sobre o salário mais os adicionais de manutenção caso a casa seja fornecida.',
        'category': 'Informativos',
        'esocial_nature_code': '1623',
        'incidence': {
            'inss': False, 'fgts': False, 'irrf': False, 'risk_level': 'low',
            'inss_observation': 'O aviso prévio indenizado tem natureza indenizatória — não integra o salário de contribuição.',
            'risk_reason': 'Baixo risco de encargos. Atenção: o aviso prévio proporcional (Art. 1 Lei 12.506/2011) também se aplica ao doméstico. Calcular o prazo correto (até 90 dias para longevos) é essencial para evitar diferenças.',
        },
        'legal_basis': [{'norm_number': '150', 'norm_year': 2015, 'article': 'Art. 34 e 35', 'is_primary': True,
            'excerpt': 'O empregado doméstico adquire direito ao aviso prévio proporcional ao tempo de serviço, nos termos da Lei 12.506/2011.'}],
    },
    {
        'name': 'Doméstico — FGTS via DAE (Informativo)',
        'code': 'DFG001',
        'description': 'Depósito mensal de FGTS de 8% + 3,2% de indenização compensatória pelo empregador doméstico, exclusivamente via DAE (Documento de Arrecadação do eSocial).',
        'category': 'Informativos',
        'esocial_nature_code': '1624',
        'incidence': {
            'inss': False, 'fgts': False, 'irrf': False, 'risk_level': 'medium',
            'fgts_observation': 'O FGTS do doméstico é recolhido via DAE, não via GFIP/SEFIP. Alíquota de 8% + 3,2% (indenização compensatória = substituto da multa de 40% parcelada mensalmente).',
            'risk_reason': 'Risco médio: o DAE é amplamente desconhecido. Empregadores que recolhem FGTS doméstico via GFIP erram o veículo — o FGTS não é creditado na conta vinculada. A multa de 40% também muda: o doméstico tem o 3,2% mensal como compensação, e em caso de dispensa sem justa causa, saca tudo acumulado.',
        },
        'legal_basis': [{'norm_number': '150', 'norm_year': 2015, 'article': 'Art. 22 e Art. 23', 'is_primary': True,
            'excerpt': 'É obrigatório o recolhimento, no Simples Doméstico, das contribuições previdenciárias e do FGTS por meio do Documento de Arrecadação do eSocial — DAE, gerado pelo Portal do eSocial.'}],
    },

    # ── Descontos especiais ─────────────────────────────────────────────────────
    {
        'name': 'Desconto de Alimentação (PAT)',
        'code': 'DAP001',
        'description': 'Desconto efetuado do empregado no programa PAT — valor de coparticipação descontado mensalmente pelo fornecimento de refeições ou alimentação. Redutor da base do IRRF.',
        'category': 'Descontos',
        'esocial_nature_code': '9150',
        'incidence': {
            'inss': False, 'fgts': False, 'irrf': False, 'risk_level': 'low',
            'irrf_observation': 'A coparticipação do empregado no PAT é dedutível da base do IRRF, pois o benefício em si não é considerado salário. Limite de desconto: máximo de 20% do custo do fornecimento.',
            'risk_reason': 'Baixo risco. A empresa deve estar inscrita no PAT para que o benefício seja não salarial. Sem inscrição ativa no PAT, o benefício passa a ter natureza salarial (vide SIA001).',
        },
        'legal_basis': [{'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943, 'article': 'Art. 458, par. 2, III c/c Lei 6.321/1976', 'is_primary': True,
            'excerpt': 'Não serão considerados como salário os programas de alimentação aprovados pelo Ministério do Trabalho e Emprego, nos termos da Lei 6.321, de 14 de abril de 1976.'}],
    },
    {
        'name': 'Desconto de Plano de Saúde (Empregado)',
        'code': 'PSA001',
        'description': 'Coparticipação do empregado no plano de saúde coletivo empresarial, descontada mensalmente em folha. Reduz a base do IRRF quando o plano é coletivo.',
        'category': 'Descontos',
        'esocial_nature_code': '9150',
        'incidence': {
            'inss': False, 'fgts': False, 'irrf': False, 'risk_level': 'low',
            'irrf_observation': 'Prêmios de plano de saúde pago pelo empregado são dedutíveis do IRRF, conforme Instrução Normativa SRF 15/2001 — apenas quando o plano é coletivo e regulado pela ANS.',
            'risk_reason': 'Baixo risco. Atenção: planos individuais não são dedutíveis na fonte pelo empregador, apenas na Declaração Anual. Garantir que o plano seja coletivo empresarial para dedubitilidade mensal.',
        },
        'legal_basis': [{'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943, 'article': 'IN SRF 15/2001 c/c Decreto 9.580/2018 Art. 68', 'is_primary': True,
            'excerpt': 'São dedutíveis da base de cálculo do imposto de renda os pagamentos efetuados pelo contribuinte a planos de saúde coletivos, empresariais ou por adesão, destinados à cobertura de despesas médicas, odontológicas e hospitalares.'}],
    },

    # ── Teletrabalho ───────────────────────────────────────────────────────────
    {
        'name': 'Teletrabalho — Ressarcimento de Despesas',
        'code': 'TEL001',
        'description': 'Reembolso de despesas do empregado em teletrabalho (energia elétrica, internet, equipamentos). Não tem natureza salarial quando devidamente documentado e previsto em contrato.',
        'category': 'Informativos',
        'esocial_nature_code': '1210',
        'incidence': {
            'inss': False, 'fgts': False, 'irrf': False, 'risk_level': 'medium',
            'inss_observation': 'O ressarcimento de despesas de teletrabalho não integra o salário de contribuição, desde que haja previsão contratual (Art. 75-D CLT) e comprovação das despesas.',
            'risk_reason': 'Risco médio: o pagamento de auxílio fixo de home office sem comprovação de despesas pode ser recaracterizado como salário. A Reforma Trabalhista (2017) criou o Art. 75-D mas exige formalização em contrato escrito. Recomenda-se manter política clara de ressarcimento com teto e comprovantes.',
        },
        'legal_basis': [{'norm_number': 'Decreto-Lei 5.452', 'norm_year': 1943, 'article': 'Art. 75-D', 'is_primary': True,
            'excerpt': 'As disposições relativas à responsabilidade pela aquisição, manutenção ou fornecimento dos equipamentos tecnológicos e da infraestrutura necessária e adequada à prestação do trabalho remoto, bem como ao reembolso de despesas arcadas pelo empregado, serão previstas em contrato escrito.'}],
    },
]


class Command(BaseCommand):
    help = 'Seed v1.3 — adiciona 30 rubricas (encargos patronais, jornada, rescisório, indenizações judiciais, intermitente, doméstico, teletrabalho)'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        from apps.catalog.models import Category, EsocialNature, Rubric
        from apps.legislation.models import LegalNorm, LegalBasis
        from apps.engine.models import Incidence

        self.stdout.write('Criando naturezas eSocial v1.3...')
        for data in V13_NATURES:
            EsocialNature.objects.get_or_create(
                code=data['code'],
                defaults={
                    'description': data['description'],
                    'is_salary_nature': data['is_salary_nature'],
                }
            )

        self.stdout.write('Criando normas legais v1.3...')
        norm_map = {}
        for norm in LegalNorm.objects.all():
            norm_map[(norm.number, norm.year)] = norm

        for data in V13_NORMS:
            norm, _ = LegalNorm.objects.get_or_create(
                number=data['number'],
                year=data['year'],
                defaults=data
            )
            norm_map[(data['number'], data['year'])] = norm

        self.stdout.write('Criando rubricas v1.3...')
        created_count = 0
        for r in RUBRICAS_V13:
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
