from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0002_add_iss_to_incidence'),
    ]

    operations = [
        migrations.AddField(
            model_name='incidence',
            name='risk_reason',
            field=models.TextField(
                blank=True,
                verbose_name='Motivo do Risco',
                help_text='Explica por que este nível de risco foi atribuído '
                          '(ex: depende de convenção coletiva, interpretação divergente na jurisprudência)'
            ),
        ),
    ]
