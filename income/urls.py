from django.urls import path
from . import views


urlpatterns = [
    path('yearly-income/', views.YearlyIncomeApiView.as_view(), name='yearly-income'),
    path('profit-summary/', views.ProfitApiView.as_view(), name='profit'),
]
