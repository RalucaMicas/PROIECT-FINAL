from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('set_buget/', views.set_buget, name='set_buget'),
    path('add_expense/', views.add_expense, name='add_expense'),
    path('summarize_expenses/', views.summarize_expenses, name='summarize_expenses'),
    path('summary_over_time/', views.summary_over_time, name='summary_over_time'),
    path('logout/', views.custom_logout, name='logout'),
    path('login/', views.custom_login, name='login'),
    path('', views.dashboard, name='dashboard'),
]