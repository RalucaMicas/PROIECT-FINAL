# Generated by Django 5.0.6 on 2024-07-18 12:03

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance_app', '0009_buget_user_expense_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='buget',
            constraint=models.UniqueConstraint(fields=('user', 'month'), name='unique_user_month'),
        ),
    ]
