# Generated by Django 4.1 on 2023-03-01 12:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Prediction', '0003_alter_parameters_loudness'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='parameters',
            name='explicit',
        ),
    ]