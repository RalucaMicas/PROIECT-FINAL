# Generated by Django 5.0.6 on 2024-07-11 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buget',
            name='month',
            field=models.CharField(max_length=7, unique=True),
        ),
    ]
