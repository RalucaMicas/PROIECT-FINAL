from sqlite3 import Date

from django.db import models

from django.contrib.auth.models import User

from django.contrib.auth import get_user_model

def get_default_user():
    User = get_user_model()
    default_user = User.objects.first()
    if default_user:
        return default_user.id # type: ignore
    else:
        new_user = User.objects.create(username='defaultuser', password='defaultpassword')
    return new_user.id # type: ignore

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=get_default_user)
    name = models.CharField(max_length=255)
    amount = models.FloatField()
    category = models.CharField(max_length=255)
    date = models.DateField(default=Date.today)

    def __str__(self):
        return f'{self.name} - {self.amount} - {self.category} - {self.date}'

class Buget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=get_default_user)
    month = models.CharField(max_length=7, unique=True)
    buget = models.FloatField(default=0.0)

    def __str__(self):
        return f'{self.month} - {self.buget}'
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'month'], name='unique_user_month')
        ]