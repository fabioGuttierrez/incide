# -*- coding: utf-8 -*-
"""
Data migration: substitui os códigos inventados de EsocialNature
pela Tabela 03 oficial do eSocial (194 códigos ativos) e remapeia
todas as rubricas existentes para os códigos oficiais corretos.
"""
import logging

from django.db import migrations

logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────────────────────
# Tabela 03 oficial do eSocial — versão 10
# Extraída em 2026-04-09 de https://frontend.esocial.gov.br/adm/
# Formato: (code, description, is_salary_nature)
# is_salary_nature conforme Art. 28 da Lei 8.212/1991
# ──────────────────────────────────────────────────────────────
OFFICIAL_NATURES = [
    ('1000', 'Salário, vencimento, soldo', True),
    ('1001', 'Subsídio', True),
    ('1003', 'Horas extraordinárias', True),
    ('1004', 'Horas extraordinárias - Banco de horas', True),
    ('1005', 'Direito de arena', True),
    ('1006', 'Intervalos intra e inter jornadas não concedidos', True),
    ('1007', 'Luvas e premiações', True),
    ('1009', 'Salário-família - Complemento', True),
    ('1010', 'Salário in natura - Pagos em bens ou serviços', True),
    ('1011', 'Sobreaviso e prontidão', True),
    ('1012', 'Descanso semanal remunerado - DSR e feriado', True),
    ('1015', 'Adiantamento de férias', True),
    ('1016', 'Férias', True),
    ('1017', 'Terço constitucional de férias', True),
    ('1018', 'Férias - Abono ou gratificação de férias superior a 20 dias', True),
    ('1019', 'Terço constitucional de férias - Abono ou gratificação de férias superior a 20 dias', True),
    ('1022', 'Férias - Abono ou gratificação de férias não excedente a 20 dias', True),
    ('1023', 'Férias - Abono pecuniário', True),
    ('1024', 'Férias - Dobro na vigência do contrato', True),
    ('1040', 'Licença-prêmio', True),
    ('1041', 'Licença-prêmio indenizada', True),
    ('1050', 'Remuneração de dias de afastamento', True),
    ('1080', 'Stock option', True),
    ('1099', 'Outras verbas salariais', True),
    ('1201', 'Adicional de função / cargo confiança', True),
    ('1202', 'Adicional de insalubridade', True),
    ('1203', 'Adicional de periculosidade', True),
    ('1204', 'Adicional de transferência', True),
    ('1205', 'Adicional noturno', True),
    ('1206', 'Adicional por tempo de serviço', True),
    ('1207', 'Comissões, porcentagens, produção', True),
    ('1208', 'Gueltas ou gorjetas - Repassadas por fornecedores ou clientes', True),
    ('1209', 'Gueltas ou gorjetas - Repassadas pelo empregador', True),
    ('1210', 'Gratificação por acordo ou convenção coletiva', True),
    ('1211', 'Gratificações', True),
    ('1212', 'Gratificações ou outras verbas de natureza permanente', True),
    ('1213', 'Gratificações ou outras verbas de natureza transitória', True),
    ('1214', 'Adicional de penosidade', True),
    ('1215', 'Adicional de unidocência', True),
    ('1216', 'Adicional de localidade', True),
    ('1217', 'Gratificação de curso/concurso', True),
    ('1225', 'Quebra de caixa', True),
    ('1230', 'Remuneração do dirigente sindical', True),
    ('1299', 'Outros adicionais', True),
    ('1300', 'PLR - Participação em Lucros ou Resultados', False),
    ('1350', 'Bolsa de estudo - Estagiário', False),
    ('1351', 'Bolsa de estudo - Médico residente', False),
    ('1352', 'Bolsa de estudo ou pesquisa', False),
    ('1401', 'Abono', False),
    ('1402', 'Abono PIS/PASEP', False),
    ('1403', 'Abono legal', False),
    ('1404', 'Auxílio babá', False),
    ('1405', 'Assistência médica', False),
    ('1406', 'Auxílio-creche', False),
    ('1407', 'Auxílio-educação', False),
    ('1409', 'Salário-família', False),
    ('1410', 'Auxílio - Locais de difícil acesso', False),
    ('1411', 'Auxílio-natalidade', False),
    ('1412', 'Abono permanência', False),
    ('1601', 'Ajuda de custo - Aeronauta', False),
    ('1602', 'Ajuda de custo de transferência', False),
    ('1603', 'Ajuda de custo', False),
    ('1619', 'Ajuda compensatória - Programa Emergencial de Manutenção do Emprego e da Renda', False),
    ('1620', 'Ressarcimento de despesas pelo uso de veículo próprio', False),
    ('1621', 'Ressarcimento de despesas de viagem, exceto despesas com veículos', False),
    ('1623', 'Ressarcimento de provisão', False),
    ('1629', 'Ressarcimento de outras despesas', False),
    ('1650', 'Diárias de viagem', False),
    ('1799', 'Alimentação concedida em pecúnia com caráter indenizatório', False),
    ('1800', 'Alimentação concedida em pecúnia com caráter salarial', True),
    ('1802', 'Etapas (marítimos)', True),
    ('1805', 'Moradia', True),
    ('1806', 'Alimentação em ticket ou cartão, vinculada ao PAT', False),
    ('1807', 'Alimentação em ticket ou cartão, não vinculada ao PAT', True),
    ('1808', 'Cesta básica ou refeição, vinculada ao PAT', False),
    ('1809', 'Cesta básica ou refeição, não vinculada ao PAT', True),
    ('1810', 'Vale-transporte ou auxílio-transporte com caráter indenizatório', False),
    ('1811', 'Auxílio-transporte ou auxílio-combustível com caráter salarial', True),
    ('1899', 'Outros auxílios', False),
    ('1901', 'Juros e/ou atualização monetária', False),
    ('2501', 'Prêmios', False),
    ('2510', 'Direitos autorais e intelectuais', False),
    ('2801', 'Quarentena remunerada', False),
    ('2901', 'Empréstimos', False),
    ('2903', 'Vestuário e equipamentos', False),
    ('2930', 'Insuficiência de saldo', False),
    ('2999', 'Arredondamentos', False),
    ('3501', 'Remuneração por prestação de serviços', True),
    ('3505', 'Retiradas (pró-labore) de diretores empregados', True),
    ('3506', 'Retiradas (pró-labore) de diretores não empregados', True),
    ('3508', 'Retiradas (pró-labore) de proprietários ou sócios', True),
    ('3509', 'Honorários a conselheiros', True),
    ('3510', 'Gratificação (jeton)', True),
    ('3511', 'Gratificação eleitoral', True),
    ('3520', 'Remuneração de cooperado', True),
    ('3525', 'Côngruas, prebendas e afins', True),
    ('4010', 'Complementação salarial de auxílio-doença', True),
    ('4011', 'Complemento de salário-mínimo - RPPS', True),
    ('4050', 'Salário-maternidade', True),
    ('4051', 'Salário-maternidade - 13° salário', True),
    ('5001', '13º salário', True),
    ('5005', '13° salário complementar', True),
    ('5501', 'Adiantamento de salário', False),
    ('5504', '13º salário - Adiantamento', False),
    ('5510', 'Adiantamento de benefícios previdenciários', False),
    ('6000', 'Saldo de salários na rescisão contratual', True),
    ('6001', '13º salário relativo ao aviso prévio indenizado', True),
    ('6002', '13° salário proporcional na rescisão', True),
    ('6003', 'Indenização compensatória do aviso prévio', False),
    ('6004', 'Férias - Dobro na rescisão', False),
    ('6006', 'Férias proporcionais', False),
    ('6007', 'Férias vencidas na rescisão', False),
    ('6101', 'Indenização compensatória - Multa rescisória 20 ou 40% (CF/88)', False),
    ('6102', 'Indenização do art. 9º da Lei 7.238/1984', False),
    ('6103', 'Indenização do art. 14 da Lei 5.889/1973', False),
    ('6104', 'Indenização do art. 479 da CLT', False),
    ('6105', 'Indenização recebida a título de incentivo a demissão', False),
    ('6106', 'Multa do art. 477 da CLT', False),
    ('6107', 'Indenização por quebra de estabilidade', False),
    ('6108', 'Tempo de espera do motorista profissional', False),
    ('6119', 'Indenização rescisória - Programa Emergencial de Manutenção do Emprego e da Renda', False),
    ('6129', 'Outras verbas não remuneratórias (indenizatórias ou multas)', False),
    ('6901', 'Desconto do aviso prévio', False),
    ('6904', 'Multa prevista no art. 480 da CLT', False),
    ('7001', 'Proventos', False),
    ('7002', 'Proventos - Pensão por morte Civil', False),
    ('7003', 'Proventos - Reserva', False),
    ('7004', 'Proventos - Reforma', False),
    ('7005', 'Pensão Militar', False),
    ('7006', 'Auxílio-reclusão', False),
    ('7007', 'Pensões especiais', False),
    ('7008', 'Complementação de aposentadoria/ pensão', False),
    ('9200', 'Desconto de adiantamentos', False),
    ('9201', 'Contribuição previdenciária', False),
    ('9202', 'Contribuição militar', False),
    ('9203', 'Imposto de Renda Retido na Fonte', False),
    ('9205', 'Provisão de contribuição previdenciária', False),
    ('9207', 'Faltas', False),
    ('9208', 'Atrasos', False),
    ('9209', 'Faltas ou atrasos', False),
    ('9210', 'DSR s/faltas e atrasos', False),
    ('9211', 'DSR sobre faltas', False),
    ('9212', 'DSR sobre atrasos', False),
    ('9213', 'Pensão alimentícia', False),
    ('9214', '13° salário - Desconto de adiantamento', False),
    ('9216', 'Desconto de vale-transporte', False),
    ('9217', 'Contribuição a Outras Entidades e Fundos', False),
    ('9218', 'Retenções judiciais', False),
    ('9219', 'Desconto de assistência médica ou odontológica - Plano coletivo empresarial', False),
    ('9221', 'Desconto de férias', False),
    ('9222', 'Desconto de outros impostos e contribuições', False),
    ('9223', 'Previdência complementar - Parte do empregado', False),
    ('9224', 'FAPI - Parte do empregado', False),
    ('9225', 'Previdência complementar - Parte do servidor', False),
    ('9226', 'Desconto de férias - Abono', False),
    ('9230', 'Contribuição sindical laboral', False),
    ('9231', 'Mensalidade sindical ou associativa', False),
    ('9232', 'Contribuição sindical - Assistencial', False),
    ('9233', 'Contribuição sindical - Confederativa', False),
    ('9240', 'Alimentação concedida em pecúnia - Desconto', False),
    ('9241', 'Alimentação em ticket ou cartão, vinculada ao PAT - Desconto', False),
    ('9242', 'Alimentação em ticket ou cartão, não vinculada ao PAT - Desconto', False),
    ('9243', 'Cesta básica ou refeição, vinculada ao PAT - Desconto', False),
    ('9244', 'Cesta básica ou refeição, não vinculada ao PAT - Desconto', False),
    ('9250', 'Seguro de vida - Desconto', False),
    ('9253', 'Empréstimos eConsignado - Desconto', False),
    ('9254', 'Empréstimos consignados - Desconto', False),
    ('9255', 'Empréstimos do empregador - Desconto', False),
    ('9258', 'Convênios', False),
    ('9260', 'FIES - Desconto', False),
    ('9270', 'Danos e prejuízos causados pelo trabalhador', False),
    ('9291', 'Abate-teto', False),
    ('9292', 'Ressarcimento ao erário', False),
    ('9293', 'Honorários advocatícios', False),
    ('9294', 'Redutor EC 41/03', False),
    ('9299', 'Outros descontos', False),
    ('9901', 'Base de cálculo da contribuição previdenciária', False),
    ('9902', 'Total da base de cálculo do FGTS', False),
    ('9903', 'Total da base de cálculo do IRRF', False),
    ('9904', 'Total da base de cálculo do FGTS rescisório', False),
    ('9905', 'Serviço militar', False),
    ('9906', 'Remuneração no exterior', False),
    ('9907', 'Total da contribuição da previdenciária patronal - RPPS', False),
    ('9908', 'FGTS - Depósito', False),
    ('9910', 'Seguros', False),
    ('9911', 'Assistência Médica', False),
    ('9912', 'Desconto de assistência médica ou odontológica - Plano diferente de coletivo empresarial', False),
    ('9930', 'Salário-maternidade pago pela Previdência Social', False),
    ('9931', 'Salário-maternidade pago pela Previdência Social - 13° salário', False),
    ('9932', 'Auxílio-doença acidentário', False),
    ('9933', 'Auxílio-doença', False),
    ('9938', 'Isenção IRRF - 65 anos', False),
    ('9939', 'Outros valores tributáveis', False),
    ('9989', 'Outros valores informativos', False),
]

# ──────────────────────────────────────────────────────────────
# Mapeamento: rubric.code → código oficial da Tabela 03
# ──────────────────────────────────────────────────────────────
RUBRIC_MAPPING = {
    # seed_initial_data (10)
    'SAL001': '1000',
    'HE050':  '1003',
    'ANT001': '1205',
    'FER001': '1016',
    'TFE001': '1017',
    'VTD001': '9216',
    '13S002': '5001',
    'INS001': '1202',
    'SFM001': '1409',
    'ADT001': '5501',
    # seed_all_rubricas (30)
    'HE100':  '1003',
    'PER001': '1203',
    'COM001': '1207',
    'GFN001': '1201',
    'DSR001': '1012',
    'SOB001': '1011',
    'TRF001': '1204',
    '13S001': '5504',
    'FEI001': '6007',
    'TFI001': '6007',
    'APF001': '1023',
    'APT001': '1000',
    'API001': '6003',
    'SSR001': '6000',
    'MUL001': '6101',
    'IND001': '6129',
    'VRF001': '1806',
    'CEB001': '1808',
    'PLS001': '1405',
    'AUX001': '1406',
    'SEG001': '9910',
    'HOM001': '1629',
    'INSS01': '9201',
    'IRRF01': '9203',
    'VRD001': '9241',
    'PLD001': '9219',
    'PEN001': '9213',
    'PLR001': '1300',
    'AJC001': '1603',
    'DIA001': '1650',
    # seed_v11_rubricas (48)
    'HEF001': '1003',
    'DSC001': '1012',
    'BNH001': '1004',
    'INT001': '1006',
    'ITI001': '1006',
    'INS040': '1202',
    'INS020': '1202',
    'INS010': '1202',
    'PRP001': '2501',
    'GOR001': '1208',
    'GAS001': '1211',
    'BON001': '2501',
    'FPR001': '6006',
    'TFP001': '6006',
    '13SR01': '6002',
    'INS13S': '9201',
    'IRR13S': '9203',
    'ADT13S': '9214',
    'APP001': '6003',
    'MUL020': '6101',
    'FGR001': '9904',
    'RIN001': '6129',
    'IDD001': '6107',
    'FAL001': '9209',
    'DSF001': '9211',
    'CON001': '9254',
    'CSF001': '9231',
    'EDU001': '1407',
    'VCO001': '1811',
    'AFR001': '1899',
    'AMO001': '1805',
    'PVC001': '9223',
    'BINSS1': '9901',
    'BIRRF1': '9903',
    'BFGTS1': '9902',
    'FGM001': '9908',
    'MAT001': '4050',
    'PAT001': '1050',
    'ADP001': '9933',
    'ADA001': '9932',
    'AF15D1': '1050',
    'APR001': '1000',
    'EST001': '1350',
    'DOM001': '1000',
    'RPA001': '3501',
    'PPR001': '1300',
    'REM001': '1629',
    'EST002': '6107',
    # seed_v12_rubricas (20)
    'QCX001': '1225',
    'ATS001': '1206',
    'ACF001': '1201',
    'HEI001': '1006',
    'SIN001': '1010',
    'SIA001': '1010',
    'LGA001': '1050',
    'LNJ001': '1050',
    'L473001': '1050',
    'AF15A1': '1050',
    'M467001': '6129',
    'M477001': '6106',
    'IEG001': '6107',
    'IEC001': '6107',
    'PRO001': '3508',
    'STO001': '1080',
    'PVE001': '9223',
    'AUC001': '4010',
    'FED001': '1024',
    'RAT001': '9907',
    # seed_v13_rubricas (30)
    'INP001': '9907',
    'SIS001': '9217',
    'SAE001': '9217',
    'FG131':  '9908',
    'HE12X1': '1003',
    'PRT001': '1011',
    'TDB001': '1003',
    'HEN001': '1003',
    'RI479':  '6104',
    'DP480':  '6904',
    'VRJ001': '6000',
    'CMR001': '1207',
    'PDE001': '6105',
    'IDM001': '6129',
    'IAT001': '6129',
    'ILU001': '6129',
    'AAI001': '9932',
    'ABO001': '1402',
    'TIN001': '1000',
    'TI13S':  '5001',
    'TIF001': '1016',
    'CAS001': '9232',
    'TCN001': '9233',
    'D13D01': '5001',
    'DFE001': '1016',
    'DAV001': '6003',
    'DFG001': '9908',
    'DAP001': '9241',
    'PSA001': '9219',
    'TEL001': '1629',
    # seed_v14_rubricas (22)
    'ISS001': '9222',
    'PIS001': '9222',
    'CSLL01': '9222',
    'IRF001': '9203',
    'RUR001': '1000',
    'FUN001': '9217',
    'CCI001': '1000',
    'DEA001': '9908',
    'COO001': '3520',
    'COI001': '9201',
    'AFT001': '1216',
    'HOD001': '3506',
    'LIC001': '1050',
    'ACA001': '1217',
    'GYM001': '1899',
    'EAP001': '1899',
    'CAR001': '1010',
    'CEL001': '1010',
    'JET001': '3510',
    'RND001': '6000',
    'CTD001': '6000',
    'G14S1':  '1210',
}


def migrate_natures(apps, schema_editor):
    EsocialNature = apps.get_model('catalog', 'EsocialNature')
    Rubric = apps.get_model('catalog', 'Rubric')

    official_codes = {code for code, _, _ in OFFICIAL_NATURES}

    # ── Fase 1: criar/atualizar os 194 códigos oficiais ──
    for code, description, is_salary in OFFICIAL_NATURES:
        EsocialNature.objects.update_or_create(
            code=code,
            defaults={
                'description': description,
                'is_salary_nature': is_salary,
            },
        )

    # ── Fase 2: remapear rubricas ──
    remapped = 0
    skipped = 0
    for rubric in Rubric.objects.select_related('esocial_nature').all():
        new_code = RUBRIC_MAPPING.get(rubric.code)
        if not new_code:
            logger.warning(
                'Rubric %s (%s) has no mapping — skipping',
                rubric.code, rubric.name,
            )
            skipped += 1
            continue

        try:
            new_nature = EsocialNature.objects.get(code=new_code)
        except EsocialNature.DoesNotExist:
            logger.error(
                'Official code %s not found for rubric %s',
                new_code, rubric.code,
            )
            continue

        if rubric.esocial_nature_id != new_nature.id:
            rubric.esocial_nature = new_nature
            rubric.save(update_fields=['esocial_nature_id'])
            remapped += 1

    logger.info('Remapped %d rubrics, skipped %d', remapped, skipped)

    # ── Fase 3: limpar códigos inventados ──
    deleted = 0
    orphans = EsocialNature.objects.exclude(code__in=official_codes)
    for nature in orphans:
        if not Rubric.objects.filter(esocial_nature=nature).exists():
            logger.info('Deleting invented nature: %s - %s', nature.code, nature.description)
            nature.delete()
            deleted += 1
        else:
            logger.warning(
                'Invented nature %s still has rubrics — keeping',
                nature.code,
            )

    logger.info('Deleted %d invented natures', deleted)


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_add_related_rubrics'),
    ]

    operations = [
        migrations.RunPython(
            migrate_natures,
            migrations.RunPython.noop,
        ),
    ]
