from django.shortcuts import render, redirect

from .models import Expense, Buget

from .forms import ExpenseForm, BugetForm

import datetime

import calendar

from django.db.models import Sum

from django.contrib.auth import login, authenticate

from django.contrib.auth import logout

from django.shortcuts import redirect

from .forms import RegisterForm

from django.contrib.auth.decorators import login_required

from django.contrib.auth.forms import AuthenticationForm

from django.contrib import messages

import json

from django.db import IntegrityError

expense_categories = [
        '🍔 Mancare',
        '🏡 Casa',
        '💼 Munca',
        '🎉 Distractie',
        '✨ Diverse'
    ]

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect('dashboard')
    
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Nume sau parola invalide.')
        else:
            messages.error(request, 'Nume sau parola invalide.')
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})

def custom_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    return redirect('dashboard')

@login_required
def set_buget(request):
    current_month = datetime.datetime.now().strftime('%Y-%m')
    user = request.user

    try:
        buget_instance = Buget.objects.get(user=user, month=current_month)
        created = False
    except Buget.DoesNotExist:
        buget_instance = None
        created = True

    if request.method == 'POST':
        if created:
            buget_form = BugetForm(request.POST)
        else:
            buget_form = BugetForm(request.POST, instance=buget_instance)

        if buget_form.is_valid():
            buget_value = buget_form.cleaned_data['buget']
            if buget_value > 0:
                if created:
                    buget_instance = Buget(user=user, month=current_month, buget=buget_value)
                    buget_instance.save()
                else:
                    buget_form.save()
                return redirect('set_buget')
            else:
                buget_form.add_error('buget', 'Bugetul trebuie să fie mai mare decât 0.')
        else:
            print(buget_form.errors) #debug statement
    else:
        if created:
            buget_form = BugetForm()
        else:
            buget_form = BugetForm(instance=buget_instance)

    historical_buget = Buget.objects.filter(user=request.user).exclude(month=current_month)
    message = 'Bugetul pentru aceasta luna este deja stabilit!' if not created else None
    
    bugets = Buget.objects.filter(user=request.user).order_by('-month')

    context = {
        'current_month': current_month,
        'current_buget': buget_instance,
        'historical_buget': historical_buget,
        'buget_form': buget_form,
        'bugets':bugets,
        'message': message,
    }

    return render(request, 'finance_app/set_buget.html', context)

@login_required
def add_expense(request):
    if request.method == 'POST':
        expense_form = ExpenseForm(request.POST)
        if expense_form.is_valid():
            expense = expense_form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('add_expense')
    else:
        expense_form = ExpenseForm()

    expenses = Expense.objects.filter(user=request.user).order_by('-date')

    context = {
        'expense_form': expense_form,
        'expenses': expenses,
    }
    
    return render(request, 'finance_app/add_expense.html', context)

@login_required
def summarize_expenses(request):
    current_month = datetime.datetime.now().strftime('%Y-%m')
    year, month = map(int, current_month.split('-'))

    expenses = Expense.objects.filter(user=request.user, date__year=year, date__month=month)
    buget = Buget.objects.filter(user=request.user, month=current_month).first()

    if not expenses.exists():
        return render(request, 'finance_app/summarize_expenses.html', {'message': 'Nu exista cheltuieli inregistrate pentru aceasta luna.'})

    total_spent = expenses.aggregate(Sum('amount'))['amount__sum'] or 0

    amount_by_category = {}
    detailed_expenses_by_category = {}

    for expense in expenses:
        if expense.category in amount_by_category:
            amount_by_category[expense.category] += expense.amount
            detailed_expenses_by_category[expense.category].append(expense)
        else:
            amount_by_category[expense.category] = expense.amount
            detailed_expenses_by_category[expense.category] = [expense]

    expense_categories = Expense.objects.values_list('category', flat=True).distinct()

    for category in expense_categories:
        if category not in amount_by_category:
            amount_by_category[category] = 0
            detailed_expenses_by_category[category] = []

    remaining_buget = buget.buget - total_spent if buget else 0
    now = datetime.datetime.now()
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    remaining_days = days_in_month - now.day
    daily_buget = remaining_buget / remaining_days if remaining_days > 0 else 0

    categories = list(amount_by_category.keys())
    category_amount = list(amount_by_category.values())
    percentages = [(amount / total_spent) * 100 if total_spent > 0 else 0 for amount in category_amount]

    context = {
        'expenses': expenses,
        'amount_by_category': amount_by_category,
        'detailed_expenses_by_category': detailed_expenses_by_category,
        'total_spent': total_spent,
        'remaining_buget': remaining_buget,
        'daily_buget': daily_buget,
        'categories': json.dumps(categories),
        'percentages': json.dumps(percentages),
        'user': request.user,
    }

    return render(request, 'finance_app/summarize_expenses.html', context)

@login_required
def summary_over_time(request):
    today = datetime.date.today()
    current_year = today.year
    current_month = today.month

    all_bugets = Buget.objects.filter(user=request.user).order_by('month')
    all_expenses = Expense.objects.filter(user=request.user).order_by('date')

    summary = {}

    for buget in all_bugets:
        year, month = map(int, buget.month.split('-'))
        expenses_for_month = all_expenses.filter(date__year=year, date__month=month)

        total_spent = expenses_for_month.aggregate(Sum('amount'))['amount__sum'] or 0
        initial_buget = buget.buget
        remaining_buget = initial_buget - total_spent

        summary[buget.month] = {
            'initial_buget': initial_buget,
            'total_spent':total_spent,
            'remaining_buget': remaining_buget,
            'details_by_category': expenses_for_month.values('category').annotate(total=Sum('amount'))
        }

    context = {
        'summary': summary,
    }

    return render(request, 'finance_app/summary_over_time.html', context)

def dashboard(request):
    return render(request, 'finance_app/dashboard.html')