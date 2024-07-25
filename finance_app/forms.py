from django import forms

from .models import Expense, Buget

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Introdu o adresa de email valida (camp obligatoriu).')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

expense_categories = [
    ('🍔 Mancare', '🍔 Mancare'),
    ('🏡 Casa', '🏡 Casa'),
    ('💼 Munca', '💼 Munca'),
    ('🎉 Distractie', '🎉 Distractie'),
    ('✨ Diverse', '✨ Diverse'),
]

class ExpenseForm(forms.ModelForm):
    category = forms.ChoiceField(choices=expense_categories, label='Categorie')
    name = forms.CharField(label='Nume')
    amount = forms.FloatField(label='Suma')
    date = forms.DateField(label='Data', widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Expense
        fields = ['name', 'amount', 'category', 'date']

class BugetForm(forms.ModelForm):
    class Meta:
        model = Buget
        fields = ['buget']
    
    def clean_buget(self):
        buget = self.cleaned_data.get('buget')
        if buget is None or buget <= 0:
            raise forms.ValidationError("Bugetul trebuie să fie mai mare decât 0.")
        return buget