# Generated by Django 4.1 on 2023-03-03 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Prediction', '0005_prediction_popularity_prediction_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='parameters',
            name='genre',
            field=models.CharField(max_length=80, null=True),
        ),
        migrations.AddField(
            model_name='prediction',
            name='genre',
            field=models.CharField(max_length=80, null=True),
        ),
    ]
