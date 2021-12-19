from django.shortcuts import render
from .models import Expense
from datetime import datetime
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from account.authentication import Authentication
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    ExpenseSerializer,
    AddExpenseSerializer
)

from rest_framework.generics import (
    ListAPIView,
    UpdateAPIView
)


class ExpenseInYear(APIView):
    authentication_classes = [Authentication]
    permission_classes     = [IsAuthenticated]
    serializer_class       = ExpenseSerializer

    def get(self, *args, **kwargs):
        date                  = datetime.now()
        year                  = self.request.GET.get("year")
        if year:
            expenses              = Expense.objects.filter(timestamp__year=date.year)
            total_expense_in_year = sum(expense.expense_amount for expense in expenses)
            jan_expenses          = Expense.objects.filter(timestamp__month=1, timestamp__year=year)
            feb_expenses          = Expense.objects.filter(timestamp__month=2, timestamp__year=year)
            march_expenses        = Expense.objects.filter(timestamp__month=3, timestamp__year=year)
            april_expenses        = Expense.objects.filter(timestamp__month=4, timestamp__year=year)
            may_expenses          = Expense.objects.filter(timestamp__month=5, timestamp__year=year)
            june_expenses         = Expense.objects.filter(timestamp__month=6, timestamp__year=year)
            july_expenses         = Expense.objects.filter(timestamp__month=7, timestamp__year=year)
            aug_expenses          = Expense.objects.filter(timestamp__month=8, timestamp__year=year)
            sep_expenses          = Expense.objects.filter(timestamp__month=9, timestamp__year=year)
            oct_expenses          = Expense.objects.filter(timestamp__month=10, timestamp__year=year)
            nov_expenses          = Expense.objects.filter(timestamp__month=11, timestamp__year=year)
            dec_expenses          = Expense.objects.filter(timestamp__month=12, timestamp__year=year)

            jan_total_expense     = sum(expense.expense_amount for expense in jan_expenses)
            feb_total_expense     = sum(expense.expense_amount for expense in feb_expenses)
            march_total_expense   = sum(expense.expense_amount for expense in march_expenses)
            april_total_expense   = sum(expense.expense_amount for expense in april_expenses)
            may_total_expense     = sum(expense.expense_amount for expense in may_expenses)
            june_total_expense    = sum(expense.expense_amount for expense in june_expenses)
            july_total_expense    = sum(expense.expense_amount for expense in july_expenses)
            aug_total_expense     = sum(expense.expense_amount for expense in aug_expenses)
            sep_total_expense     = sum(expense.expense_amount for expense in sep_expenses)
            oct_total_expense     = sum(expense.expense_amount for expense in oct_expenses)
            nov_total_expense     = sum(expense.expense_amount for expense in nov_expenses)
            dec_total_expense     = sum(expense.expense_amount for expense in dec_expenses)
            expense_summary = [

                {"month": "January", "year": year, "monthly_expense": jan_total_expense},
                {"month": "February", "year": year, "monthly_expense": feb_total_expense},
                {"month": "March", "year": year, "monthly_expense": march_total_expense},
                {"month": "April", "year": year, "monthly_expense": april_total_expense},
                {"month": "May", "year": year, "monthly_expense": may_total_expense},
                {"month": "June", "year": year, "monthly_expense": june_total_expense},
                {"month": "July", "year": year, "monthly_expense": july_total_expense},
                {"month": "August", "year": year, "monthly_expense": aug_total_expense},
                {"month": "September", "year": year, "monthly_expense": sep_total_expense},
                {"month": "October", "year": year, "monthly_expense": oct_total_expense},
                {"month": "November", "year": year, "monthly_expense": nov_total_expense},
                {"month": "December", "year": year, "monthly_expense": dec_total_expense}

            ]
            return Response({"data": expense_summary, "total_expense_in_year": total_expense_in_year, "year": year}, status=status.HTTP_200_OK)

        expenses              = Expense.objects.filter(timestamp__year=date.year)
        total_expense_in_year = sum(expense.expense_amount for expense in expenses)
        jan_expenses          = Expense.objects.filter(timestamp__month=1, timestamp__year=date.year)
        feb_expenses          = Expense.objects.filter(timestamp__month=2, timestamp__year=date.year)
        march_expenses        = Expense.objects.filter(timestamp__month=3, timestamp__year=date.year)
        april_expenses        = Expense.objects.filter(timestamp__month=4, timestamp__year=date.year)
        may_expenses          = Expense.objects.filter(timestamp__month=5, timestamp__year=date.year)
        june_expenses         = Expense.objects.filter(timestamp__month=6, timestamp__year=date.year)
        july_expenses         = Expense.objects.filter(timestamp__month=7, timestamp__year=date.year)
        aug_expenses          = Expense.objects.filter(timestamp__month=8, timestamp__year=date.year)
        sep_expenses          = Expense.objects.filter(timestamp__month=9, timestamp__year=date.year)
        oct_expenses          = Expense.objects.filter(timestamp__month=10, timestamp__year=date.year)
        nov_expenses          = Expense.objects.filter(timestamp__month=11, timestamp__year=date.year)
        dec_expenses          = Expense.objects.filter(timestamp__month=12, timestamp__year=date.year)

        jan_total_expense     = sum(expense.expense_amount for expense in jan_expenses)
        feb_total_expense     = sum(expense.expense_amount for expense in feb_expenses)
        march_total_expense   = sum(expense.expense_amount for expense in march_expenses)
        april_total_expense   = sum(expense.expense_amount for expense in april_expenses)
        may_total_expense     = sum(expense.expense_amount for expense in may_expenses)
        june_total_expense    = sum(expense.expense_amount for expense in june_expenses)
        july_total_expense    = sum(expense.expense_amount for expense in july_expenses)
        aug_total_expense     = sum(expense.expense_amount for expense in aug_expenses)
        sep_total_expense     = sum(expense.expense_amount for expense in sep_expenses)
        oct_total_expense     = sum(expense.expense_amount for expense in oct_expenses)
        nov_total_expense     = sum(expense.expense_amount for expense in nov_expenses)
        dec_total_expense     = sum(expense.expense_amount for expense in dec_expenses)

        expense_summary = [

            {"month": "January", "year": date.year, "monthly_expense": jan_total_expense},
            {"month": "February", "year": date.year, "monthly_expense": feb_total_expense},
            {"month": "March", "year": date.year, "monthly_expense": march_total_expense},
            {"month": "April", "year": date.year, "monthly_expense": april_total_expense},
            {"month": "May", "year": date.year, "monthly_expense": may_total_expense},
            {"month": "June", "year": date.year, "monthly_expense": june_total_expense},
            {"month": "July", "year": date.year, "monthly_expense": july_total_expense},
            {"month": "August", "year": date.year, "monthly_expense": aug_total_expense},
            {"month": "September", "year": date.year, "monthly_expense": sep_total_expense},
            {"month": "October", "year": date.year, "monthly_expense": oct_total_expense},
            {"month": "November", "year": date.year, "monthly_expense": nov_total_expense},
            {"month": "December", "year": date.year, "monthly_expense": dec_total_expense}

        ]
        return Response({"data": expense_summary, "total_expense_in_year": total_expense_in_year, "year": date.year}, status=status.HTTP_200_OK)




class MonthlyExpenseApiView(APIView):
    authentication_classes = [Authentication]
    permission_classes     = [IsAuthenticated]
    serializer_class       = ExpenseSerializer

    def get(self, *args, **kwargs):
        timestamp       = self.request.GET.get("timestamp")
        requested_month = str(kwargs['month'])
        month_obj       = datetime.strptime(requested_month, "%B")
        get_moth        = month_obj.month
        expenses        = Expense.objects.filter(timestamp__year=kwargs["year"], timestamp__month=get_moth)
        if timestamp:
            year          = int(timestamp[0:4])
            month         = int(timestamp[5:7])
            day           = int(timestamp[8:12])
            expenses      = expenses.filter(timestamp__year=year, timestamp__month=month, timestamp__day=day + 1)
            total_expense = sum(expense.expense_amount for expense in expenses)
            serializer    = self.serializer_class(expenses, many=True)
            return Response({"data": serializer.data, "total_expense": total_expense}, status=status.HTTP_200_OK)
        else:
            expenses      = Expense.objects.filter(timestamp__year=kwargs["year"], timestamp__month=get_moth)
            total_expense = sum(expense.expense_amount for expense in expenses)
            serializer    = self.serializer_class(expenses, many=True)
            return Response({"data": serializer.data, "total_expense": total_expense}, status=status.HTTP_200_OK)



class TodayExpensesApiView(APIView):
    authentication_classes = [Authentication]
    permission_classes     = [IsAuthenticated]
    serializer_class       = ExpenseSerializer

    def get(self, *args, **kwargs):
        date          = datetime.now()
        expenses      = Expense.objects.filter(timestamp__year=date.year, timestamp__month=date.month, timestamp__day=date.day)
        serializer    = self.serializer_class(expenses, many=True)
        total_expense = sum(expense.expense_amount for expense in expenses)
        return Response({"data": serializer.data, "total_expense": total_expense}, status=status.HTTP_200_OK)




class AddExpenseApiView(APIView):
    authentication_classes = [Authentication]
    permission_classes     = [IsAuthenticated]
    serializer_class = AddExpenseSerializer

    def post(self, *args, **kwargs):
        serializer  = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        saved_data  = serializer.save(entry_by=self.request.user, creator_name=self.request.user.username)
        serializer2 = ExpenseSerializer(saved_data, many=False)
        return Response({"data": serializer2.data, "total_expense": saved_data.expense_amount}, status=status.HTTP_201_CREATED)



class UpdateExpenseApiView(APIView):
    authentication_classes = [Authentication]
    permission_classes     = [IsAuthenticated]
    queryset               = Expense.objects.all()
    serializer_class       = AddExpenseSerializer


    def post(self, *args, **kwargs):
        try:
            expense = Expense.objects.get(id=kwargs["id"])
        except Exception as e:
            return Response({"error": "Query does not exists !"})
        serializer  = self.serializer_class(instance=expense, data=self.request.data)
        serializer.is_valid(raise_exception=True)
        saved_data  = serializer.save()
        serializer2 = ExpenseSerializer(saved_data, many=False)
        return Response({"data": serializer2.data, "total_expense": saved_data.expense_amount}, status=status.HTTP_200_OK)



# This class is created for Expense analytics
class ExpenseApiView(APIView):
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        date = datetime.now()
        jan_expense = 0
        feb_expense = 0
        march_expense = 0
        april_expense = 0
        may_expense = 0
        june_expense = 0
        july_expense = 0
        aug_expense = 0
        sep_expense = 0
        oct_expense = 0
        nov_expense = 0
        dec_expense = 0
        expense_summary = {}

        jan_expenses = Expense.objects.filter(timestamp__month=1, timestamp__year=date.year)
        jan_expense += sum(expense.expense_amount for expense in jan_expenses)

        feb_expenses = Expense.objects.filter(timestamp__month=2, timestamp__year=date.year)
        feb_expense += sum(expense.expense_amount for expense in feb_expenses)

        march_expenses = Expense.objects.filter(timestamp__month=3, timestamp__year=date.year)
        march_expense += sum(expense.expense_amount for expense in march_expenses)

        april_expenses = Expense.objects.filter(timestamp__month=4, timestamp__year=date.year)
        april_expense += sum(expense.expense_amount for expense in april_expenses)

        may_expenses = Expense.objects.filter(timestamp__month=5, timestamp__year=date.year)
        may_expense += sum(expense.expense_amount for expense in may_expenses)

        june_expenses = Expense.objects.filter(timestamp__month=6, timestamp__year=date.year)
        june_expense += sum(expense.expense_amount for expense in june_expenses)

        july_expenses = Expense.objects.filter(timestamp__month=7, timestamp__year=date.year)
        july_expense += sum(expense.expense_amount for expense in july_expenses)

        aug_expenses = Expense.objects.filter(timestamp__month=8, timestamp__year=date.year)
        aug_expense += sum(expense.expense_amount for expense in aug_expenses)

        sep_expenses = Expense.objects.filter(timestamp__month=9, timestamp__year=date.year)
        sep_expense += sum(expense.expense_amount for expense in sep_expenses)

        oct_expenses = Expense.objects.filter(timestamp__month=10, timestamp__year=date.year)
        oct_expense += sum(expense.expense_amount for expense in oct_expenses)

        nov_expenses = Expense.objects.filter(timestamp__month=11, timestamp__year=date.year)
        nov_expense += sum(expense.expense_amount for expense in nov_expenses)

        dec_expenses = Expense.objects.filter(timestamp__month=12, timestamp__year=date.year)
        dec_expense += sum(expense.expense_amount for expense in dec_expenses)

        expense_summary.update({
            "January": jan_expense, "February": feb_expense, "March": march_expense,
            "April": april_expense, "May": may_expense, "June": june_expense,
            "July": july_expense, "August": aug_expense, "September": sep_expense,
            "October": oct_expense, "November": nov_expense, "December": dec_expense
        })

        return Response({"data": expense_summary}, status=status.HTTP_200_OK)