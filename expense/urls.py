from django.urls import path
from . import views


urlpatterns = [
    path('add-expenses/', views.AddExpenseApiView.as_view(), name='add-expenses'),
    path('update-expenses/<int:id>/', views.UpdateExpenseApiView.as_view(), name='update-expenses'),
    path('expenses-in-year/', views.ExpenseInYear.as_view(), name='expenses-in-year'),
    path('expenses-in-month/<str:month>/<str:year>/', views.MonthlyExpenseApiView.as_view(), name='expenses-in-year'),
    path('today-expenses/', views.TodayExpensesApiView.as_view(), name='today-expenses'),

    path('expense-summary/', views.ExpenseApiView.as_view(), name='expense-summary'),
]
