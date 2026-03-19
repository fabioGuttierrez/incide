"""
Atualiza o campo ISS nas incidências das rubricas que têm ISS.

Rubrics com ISS=True (autônomos, cooperativas, prestadores de serviço):
  - RPA001: Remuneração Prestador Autônomo
"""
from django.core.management.base import BaseCommand
from apps.catalog.models import Rubric
from apps.engine.models import Incidence

ISS_TRUE_CODES = [
    'RPA001',  # Remuneração Prestador Autônomo — ISS retido na fonte (LC 116/2003)
]


class Command(BaseCommand):
    help = 'Define ISS=True para rubricas de autônomos e prestadores de serviço'

    def handle(self, *args, **kwargs):
        updated = 0
        for code in ISS_TRUE_CODES:
            try:
                rubric = Rubric.objects.get(code=code)
                inc = Incidence.objects.get(rubric=rubric)
                if not inc.iss:
                    inc.iss = True
                    inc.iss_observation = 'Retido na fonte pelo tomador — alíquota conforme município (LC 116/2003)'
                    inc.save(update_fields=['iss', 'iss_observation'])
                    self.stdout.write(self.style.SUCCESS(f'  [OK] {code} — ISS atualizado'))
                    updated += 1
                else:
                    self.stdout.write(f'  [--] {code} — ISS já estava True')
            except Rubric.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'  [!]  {code} — rubrica não encontrada'))
            except Incidence.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'  [!]  {code} — incidência não encontrada'))

        self.stdout.write(self.style.SUCCESS(f'\nConcluído: {updated} rubrica(s) atualizada(s).'))
