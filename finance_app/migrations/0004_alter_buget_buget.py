# Generated by Django 5.0.6 on 2024-07-11 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance_app', '0003_alter_expense_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buget',
            name='buget',
            field=models.FloatField(default=0.0),
        ),
    ]
