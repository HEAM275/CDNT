# Generated by Django 5.1.2 on 2024-10-21 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Acuerdos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='acuerdo',
            name='estado',
            field=models.CharField(choices=[('Archivado', 'Archivado'), ('Cumplida', 'Cumplida'), ('Espera', 'Espera'), ('Incumplida', 'Incumplida'), ('Confección', 'Confección'), ('Proceso', 'Proceso')], default='Confección', max_length=20),
        ),
    ]
