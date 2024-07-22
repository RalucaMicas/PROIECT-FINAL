from expense import Expense

import datetime

import calendar

import os

import json


def main():
    print(f'Tracker-ul de cheltuieli este in desfasurare!')
    expense_file_path = 'cheltuieli.csv'
    buget_file_path = 'buget.json'

    # Get or set budget for the month
    buget = get_or_set_buget(buget_file_path)

    # Get user input - pentru cheltuieli
    expense = get_user_expense()

    # Write cheltuieli to a file
    save_expense_to_file(expense, expense_file_path)

    # Read file + sumarul cheltuielilor
    summarize_expenses(expense_file_path, buget)

def get_or_set_buget(buget_file_path):
    current_month = datetime.datetime.now().strftime('%Y-%m')

    if os.path.exists(buget_file_path):
        with open(buget_file_path, 'r') as file:
            buget_data = json.load(file)
            if buget_data.get('month') == current_month:
                return buget_data.get('buget')
            
    while True:
        try:
            buget = float(input('Introdu bugetul pentru luna curenta (RON): '))
            if buget < 0:
                print('Bugetul nu poate fi negativ. Te rugam introdu un numar valid!')
                continue
            break
        except ValueError:
            print('Eroare. Trebuie sa introduci un numar valid pentru buget!')

    with open(buget_file_path, 'w') as file:
        json.dump({'month': current_month, 'buget': buget}, file)

    return buget

def get_user_expense():
    print(f'Se preiau cheltuielile!')

    while True:
        expense_name = input('Introdu denumirea tipului de cheltuiala: '). strip()
        if expense_name:
            break
        else:
            print('Campul pentru denumirea cheltuielii nu poate fi lasat gol.')

    while True:
        try:
            expense_amount = float(input('Introdu valoarea cheltuielii: '))
            if expense_amount < 0:
                print('Valoarea cheltuielii trebuie sa fie un numar pozitiv.')
                continue
            break
        except ValueError:
            print('Eroare. Trebuie sa introduci un numar valid pentru valoarea cheltuielii!')

    expense_categories = [
        '🍔 Mancare',
        '🏡 Casa',
        '💼 Munca',
        '🎉 Distractie',
        '✨ Diverse'
    ]
    
    while True:
        print('Selecteaza o categorie: ')
        for i, category_name in enumerate(expense_categories):
            print(f' {i + 1}. {category_name}')

        value_range = f'[1 - {len(expense_categories)}]'
        selected_index = -1

        try:
            selected_index = int(input(f'Introdu numarul categoriei dorite {value_range}: ')) -1
            if selected_index in range(len(expense_categories)):
                selected_category = expense_categories[selected_index]
                new_expense = Expense(
                    name=expense_name, category=selected_category, amount=expense_amount
                )
                return new_expense
            else:
                print('Categorie invalida. Te rugam sa incerci din nou!')
        except ValueError:
            print('Eroare. Trebuie sa introduceti un numar intreg!')

        print(f'Ai selectat categoria: {expense_categories[selected_index]}')

def save_expense_to_file(expense: Expense, expense_file_path):
    print(f'Cheltuieli salvate in fisier: {expense} in {expense_file_path}')
    with open(expense_file_path, mode='a', encoding='utf-8') as file:
        file.write(f'{expense.name}, {expense.amount}, {expense.category} \n')
    

def summarize_expenses(expense_file_path, buget):
    print(f'Sumarul cheltuielilor')
    expenses: list[Expense] = []

    if os.path.exists(expense_file_path):
        with open(expense_file_path, mode='r', encoding='utf-8') as file:
             lines = file.readlines()
             for line in lines:
                if line.strip():
                    expense_name, expense_amount, expense_category = line.strip().split(', ')
                    line_expense = Expense(
                        name=expense_name, amount=float(expense_amount), category=expense_category
                    )
                    expenses.append(line_expense)

    if not expenses:
        print('Nu exista cheltuieli inregistrate.')
        return

    amount_by_category = {}
    for expense in expenses:
        key = expense.category
        if key in amount_by_category:
            amount_by_category[key] += expense.amount
        else:
            amount_by_category[key] = expense.amount

    print('Cheltuieli per categorie:')
    for key, amount in amount_by_category.items():
        print(f'  {key}: {amount:.2f} RON')

    total_spent = sum([x.amount for x in expenses])
    print(f'Ai cheltuit: {total_spent:.2f} RON')

    remaining_buget = buget - total_spent
    print(f'Buget disponibil: {remaining_buget:.2f} RON')

    if remaining_buget <= 0:
        print(red('Bugetul pentru aceasta luna a fost epuizat!'))
        return

    now = datetime.datetime.now()
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    remaining_days = days_in_month - now.day

    if remaining_days > 0:
        daily_buget = remaining_buget / remaining_days
        print(green(f'Buget zilnic disponibil: {daily_buget:.2f} RON'))
    else:
        print('Nu mai sunt zile ramase din aceasta luna.')

def green(text):
    return f'\033[92m{text}\033[0m'

def red(text):
    return f'\033[91m{text}\033[0m'

if __name__ == '__main__':
    main()