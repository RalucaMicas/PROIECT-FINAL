# Generated by Django 5.0.6 on 2024-07-17 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance_app', '0007_alter_expense_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='amount',
            field=models.FloatField(),
        ),
    ]
