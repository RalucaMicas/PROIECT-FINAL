# Generated by Django 5.0.6 on 2024-07-11 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance_app', '0004_alter_buget_buget'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
