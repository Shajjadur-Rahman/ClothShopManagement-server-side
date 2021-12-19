from django.shortcuts import render
from datetime import datetime
from order.models import Order
from rest_framework import status
from expense.models import Expense
from rest_framework.views import APIView
from rest_framework.response import Response
from account.authentication import Authentication
from rest_framework.permissions import IsAuthenticated




class YearlyIncomeApiView(APIView):
    authentication_classes = [Authentication]
    permission_classes     = [IsAuthenticated]

    def get(self, *args, **kwargs):
        date                 = datetime.now()
        year                 = self.request.GET.get("year")
        jan_profit    = 0
        jan_expense   = 0
        feb_profit    = 0
        feb_expense   = 0
        march_profit  = 0
        march_expense = 0
        april_profit  = 0
        april_expense = 0
        may_profit    = 0
        may_expense   = 0
        june_profit   = 0
        june_expense  = 0
        july_profit   = 0
        july_expense  = 0
        aug_profit    = 0
        aug_expense   = 0
        sep_profit    = 0
        sep_expense   = 0
        oct_profit    = 0
        oct_expense   = 0
        nov_profit    = 0
        nov_expense   = 0
        dec_profit    = 0
        dec_expense   = 0

        if year:
            orders_in_year        = Order.objects.filter(timestamp__year=year)
            expenses_in_year      = Expense.objects.filter(timestamp__year=year)
            total_profit_in_year  = sum(order.get_total_profit_or_loss() for order in orders_in_year)
            total_expense_in_year = sum(expense.expense_amount for expense in expenses_in_year)
            net_profit_or_loss    = total_profit_in_year - total_expense_in_year

            jan_orders         = Order.objects.filter(timestamp__month=1, timestamp__year=year)
            jan_expenses       = Expense.objects.filter(timestamp__month=1, timestamp__year=year)
            jan_expense       += sum(expense.expense_amount for expense in jan_expenses)
            for order in jan_orders:
                jan_profit    += sum(item.profit for item in order.orderItems.all())
            jan_net_profit_or_loss = jan_profit - jan_expense

            feb_orders         = Order.objects.filter(timestamp__month=2, timestamp__year=year)
            feb_expenses       = Expense.objects.filter(timestamp__month=2, timestamp__year=year)
            feb_expense       += sum(expense.expense_amount for expense in feb_expenses)
            for order in feb_orders:
                feb_profit    += sum(item.profit for item in order.orderItems.all())
            feb_net_profit_or_loss = feb_profit - feb_expense

            march_orders       = Order.objects.filter(timestamp__month=3, timestamp__year=year)
            march_expenses     = Expense.objects.filter(timestamp__month=3, timestamp__year=year)
            march_expense     += sum(expense.expense_amount for expense in march_expenses)
            for order in march_orders:
                march_profit  += sum(item.profit for item in order.orderItems.all())
            march_net_profit_or_loss = march_profit - march_expense

            april_orders       = Order.objects.filter(timestamp__month=4, timestamp__year=year)
            april_expenses     = Expense.objects.filter(timestamp__month=4, timestamp__year=year)
            april_expense     += sum(expense.expense_amount for expense in april_expenses)
            for order in april_orders:
                april_profit  += sum(item.profit for item in order.orderItems.all())
            april_net_profit_or_loss = april_profit - april_expense

            may_orders       = Order.objects.filter(timestamp__month=5, timestamp__year=year)
            may_expenses     = Expense.objects.filter(timestamp__month=5, timestamp__year=year)
            may_expense     += sum(expense.expense_amount for expense in may_expenses)
            for order in may_orders:
                may_profit  += sum(item.profit for item in order.orderItems.all())
            may_net_profit_or_loss = may_profit - may_expense

            june_orders       = Order.objects.filter(timestamp__month=6, timestamp__year=year)
            june_expenses     = Expense.objects.filter(timestamp__month=6, timestamp__year=year)
            june_expense     += sum(expense.expense_amount for expense in june_expenses)
            for order in june_orders:
                june_profit  += sum(item.profit for item in order.orderItems.all())
            june_net_profit_or_loss = june_profit - june_expense

            july_orders       = Order.objects.filter(timestamp__month=7, timestamp__year=year)
            july_expenses     = Expense.objects.filter(timestamp__month=7, timestamp__year=year)
            july_expense     += sum(expense.expense_amount for expense in july_expenses)
            for order in july_orders:
                july_profit  += sum(item.profit for item in order.orderItems.all())
            july_net_profit_or_loss = july_profit - july_expense

            aug_orders       = Order.objects.filter(timestamp__month=8, timestamp__year=year)
            aug_expenses     = Expense.objects.filter(timestamp__month=8, timestamp__year=year)
            aug_expense     += sum(expense.expense_amount for expense in aug_expenses)
            for order in aug_orders:
                aug_profit  += sum(item.profit for item in order.orderItems.all())
            aug_net_profit_or_loss = aug_profit - aug_expense

            sep_orders       = Order.objects.filter(timestamp__month=9, timestamp__year=year)
            sep_expenses     = Expense.objects.filter(timestamp__month=9, timestamp__year=year)
            sep_expense     += sum(expense.expense_amount for expense in sep_expenses)
            for order in sep_orders:
                sep_profit  += sum(item.profit for item in order.orderItems.all())
            sep_net_profit_or_loss = sep_profit - sep_expense

            oct_orders       = Order.objects.filter(timestamp__month=10, timestamp__year=year)
            oct_expenses     = Expense.objects.filter(timestamp__month=10, timestamp__year=year)
            oct_expense     += sum(expense.expense_amount for expense in oct_expenses)
            for order in oct_orders:
                oct_profit  += sum(item.profit for item in order.orderItems.all())
            oct_net_profit_or_loss = oct_profit - oct_expense

            nov_orders       = Order.objects.filter(timestamp__month=11, timestamp__year=year)
            nov_expenses     = Expense.objects.filter(timestamp__month=11, timestamp__year=year)
            nov_expense     += sum(expense.expense_amount for expense in nov_expenses)
            for order in nov_orders:
                nov_profit  += sum(item.profit for item in order.orderItems.all())
            nov_net_profit_or_loss = nov_profit - nov_expense

            dec_orders       = Order.objects.filter(timestamp__month=12, timestamp__year=year)
            dec_expenses     = Expense.objects.filter(timestamp__month=12, timestamp__year=year)
            dec_expense     += sum(expense.expense_amount for expense in dec_expenses)
            for order in dec_orders:
                dec_profit  += sum(item.profit for item in order.orderItems.all())
            dec_net_profit_or_loss = dec_profit - dec_expense

            income_summary = [
                {"month": "January", "year": year, "profit": jan_profit, "expense": jan_expense, "net_loss_profit": jan_net_profit_or_loss},
                {"month": "February", "year": year, "profit": feb_profit, "expense": feb_expense, "net_loss_profit": feb_net_profit_or_loss},
                {"month": "March", "year": year,  "profit": march_profit, "expense": march_expense, "net_loss_profit": march_net_profit_or_loss},
                {"month": "April", "year": year, "profit": april_profit, "expense": april_expense, "net_loss_profit": april_net_profit_or_loss},
                {"month": "May", "year": year, "profit": may_profit, "expense": may_expense, "net_loss_profit": may_net_profit_or_loss},
                {"month": "June", "year": year, "profit": june_profit, "expense": june_expense, "net_loss_profit": june_net_profit_or_loss},
                {"month": "July", "year": year, "profit": july_profit, "expense": july_expense, "net_loss_profit": july_net_profit_or_loss},
                {"month": "August", "year": year, "profit": aug_profit, "expense": aug_expense, "net_loss_profit": aug_net_profit_or_loss},
                {"month": "September", "year": year, "profit": sep_profit, "expense": sep_expense, "net_loss_profit": sep_net_profit_or_loss},
                {"month": "October", "year": year, "profit": oct_profit, "expense": oct_expense, "net_loss_profit": oct_net_profit_or_loss},
                {"month": "November", "year": year, "profit": nov_profit, "expense": nov_expense, "net_loss_profit": nov_net_profit_or_loss},
                {"month": "December", "year": year, "profit": dec_profit, "expense": dec_expense, "net_loss_profit": dec_net_profit_or_loss},
            ]
            return Response({"data": income_summary, "total_profit_in_year": total_profit_in_year,
                             "total_expense_in_year": total_expense_in_year, "net_profit_or_loss": net_profit_or_loss,
                             "year": year}, status=status.HTTP_200_OK)

        orders_in_year = Order.objects.filter(timestamp__year=date.year)
        expenses_in_year = Expense.objects.filter(timestamp__year=date.year)
        total_profit_in_year = sum(order.get_total_profit_or_loss() for order in orders_in_year)
        total_expense_in_year = sum(expense.expense_amount for expense in expenses_in_year)
        net_profit_or_loss = total_profit_in_year - total_expense_in_year

        jan_orders = Order.objects.filter(timestamp__month=1, timestamp__year=date.year)
        jan_expenses = Expense.objects.filter(timestamp__month=1, timestamp__year=date.year)
        jan_expense += sum(expense.expense_amount for expense in jan_expenses)
        for order in jan_orders:
            jan_profit += sum(item.profit for item in order.orderItems.all())
        jan_net_profit_or_loss = jan_profit - jan_expense

        feb_orders = Order.objects.filter(timestamp__month=2, timestamp__year=date.year)
        feb_expenses = Expense.objects.filter(timestamp__month=2, timestamp__year=date.year)
        feb_expense += sum(expense.expense_amount for expense in feb_expenses)
        for order in feb_orders:
            feb_profit += sum(item.profit for item in order.orderItems.all())
        feb_net_profit_or_loss = feb_profit - feb_expense

        march_orders = Order.objects.filter(timestamp__month=3, timestamp__year=date.year)
        march_expenses = Expense.objects.filter(timestamp__month=3, timestamp__year=date.year)
        march_expense += sum(expense.expense_amount for expense in march_expenses)
        for order in march_orders:
            march_profit += sum(item.profit for item in order.orderItems.all())
        march_net_profit_or_loss = march_profit - march_expense

        april_orders = Order.objects.filter(timestamp__month=4, timestamp__year=date.year)
        april_expenses = Expense.objects.filter(timestamp__month=4, timestamp__year=date.year)
        april_expense += sum(expense.expense_amount for expense in april_expenses)
        for order in april_orders:
            april_profit += sum(item.profit for item in order.orderItems.all())
        april_net_profit_or_loss = april_profit - april_expense

        may_orders = Order.objects.filter(timestamp__month=5, timestamp__year=date.year)
        may_expenses = Expense.objects.filter(timestamp__month=5, timestamp__year=date.year)
        may_expense += sum(expense.expense_amount for expense in may_expenses)
        for order in may_orders:
            may_profit += sum(item.profit for item in order.orderItems.all())
        may_net_profit_or_loss = may_profit - may_expense

        june_orders = Order.objects.filter(timestamp__month=6, timestamp__year=date.year)
        june_expenses = Expense.objects.filter(timestamp__month=6, timestamp__year=date.year)
        june_expense += sum(expense.expense_amount for expense in june_expenses)
        for order in june_orders:
            june_profit += sum(item.profit for item in order.orderItems.all())
        june_net_profit_or_loss = june_profit - june_expense

        july_orders = Order.objects.filter(timestamp__month=7, timestamp__year=date.year)
        july_expenses = Expense.objects.filter(timestamp__month=7, timestamp__year=date.year)
        july_expense += sum(expense.expense_amount for expense in july_expenses)
        for order in july_orders:
            july_profit += sum(item.profit for item in order.orderItems.all())
        july_net_profit_or_loss = july_profit - july_expense

        aug_orders = Order.objects.filter(timestamp__month=8, timestamp__year=date.year)
        aug_expenses = Expense.objects.filter(timestamp__month=8, timestamp__year=date.year)
        aug_expense += sum(expense.expense_amount for expense in aug_expenses)
        for order in aug_orders:
            aug_profit += sum(item.profit for item in order.orderItems.all())
        aug_net_profit_or_loss = aug_profit - aug_expense

        sep_orders = Order.objects.filter(timestamp__month=9, timestamp__year=date.year)
        sep_expenses = Expense.objects.filter(timestamp__month=9, timestamp__year=date.year)
        sep_expense += sum(expense.expense_amount for expense in sep_expenses)
        for order in sep_orders:
            sep_profit += sum(item.profit for item in order.orderItems.all())
        sep_net_profit_or_loss = sep_profit - sep_expense

        oct_orders = Order.objects.filter(timestamp__month=10, timestamp__year=date.year)
        oct_expenses = Expense.objects.filter(timestamp__month=10, timestamp__year=date.year)
        oct_expense += sum(expense.expense_amount for expense in oct_expenses)
        for order in oct_orders:
            oct_profit += sum(item.profit for item in order.orderItems.all())
        oct_net_profit_or_loss = oct_profit - oct_expense

        nov_orders = Order.objects.filter(timestamp__month=11, timestamp__year=date.year)
        nov_expenses = Expense.objects.filter(timestamp__month=11, timestamp__year=date.year)
        nov_expense += sum(expense.expense_amount for expense in nov_expenses)
        for order in nov_orders:
            nov_profit += sum(item.profit for item in order.orderItems.all())
        nov_net_profit_or_loss = nov_profit - nov_expense

        dec_orders = Order.objects.filter(timestamp__month=12, timestamp__year=date.year)
        dec_expenses = Expense.objects.filter(timestamp__month=12, timestamp__year=date.year)
        dec_expense += sum(expense.expense_amount for expense in dec_expenses)
        for order in dec_orders:
            dec_profit += sum(item.profit for item in order.orderItems.all())
        dec_net_profit_or_loss = dec_profit - dec_expense

        income_summary = [
            {"month": "January", "year": date.year, "profit": jan_profit, "expense": jan_expense,
             "net_loss_profit": jan_net_profit_or_loss},
            {"month": "February", "year": date.year, "profit": feb_profit, "expense": feb_expense,
             "net_loss_profit": feb_net_profit_or_loss},
            {"month": "March", "year": date.year, "profit": march_profit, "expense": march_expense,
             "net_loss_profit": march_net_profit_or_loss},
            {"month": "April", "year": date.year, "profit": april_profit, "expense": april_expense,
             "net_loss_profit": april_net_profit_or_loss},
            {"month": "May", "year": date.year, "profit": may_profit, "expense": may_expense,
             "net_loss_profit": may_net_profit_or_loss},
            {"month": "June", "year": date.year, "profit": june_profit, "expense": june_expense,
             "net_loss_profit": june_net_profit_or_loss},
            {"month": "July", "year": date.year, "profit": july_profit, "expense": july_expense,
             "net_loss_profit": july_net_profit_or_loss},
            {"month": "August", "year": date.year, "profit": aug_profit, "expense": aug_expense,
             "net_loss_profit": aug_net_profit_or_loss},
            {"month": "September", "year": date.year, "profit": sep_profit, "expense": sep_expense,
             "net_loss_profit": sep_net_profit_or_loss},
            {"month": "October", "year": date.year, "profit": oct_profit, "expense": oct_expense,
             "net_loss_profit": oct_net_profit_or_loss},
            {"month": "November", "year": date.year, "profit": nov_profit, "expense": nov_expense,
             "net_loss_profit": nov_net_profit_or_loss},
            {"month": "December", "year": date.year, "profit": dec_profit, "expense": dec_expense,
             "net_loss_profit": dec_net_profit_or_loss},
        ]
        return Response({"data": income_summary, "total_profit_in_year": total_profit_in_year,
                         "total_expense_in_year": total_expense_in_year, "net_profit_or_loss": net_profit_or_loss,
                         "year": date.year}, status=status.HTTP_200_OK)




# This class is created for Profit analytics
class ProfitApiView(APIView):
    authentication_classes = [Authentication]
    permission_classes     = [IsAuthenticated]

    def get(self, *args, **kwargs):
        date = datetime.now()
        jan_profit    = 0
        feb_profit    = 0
        march_profit  = 0
        april_profit  = 0
        may_profit    = 0
        june_profit   = 0
        july_profit   = 0
        aug_profit    = 0
        sep_profit    = 0
        oct_profit    = 0
        nov_profit    = 0
        dec_profit    = 0
        profit_summary = {}
        jan_orders = Order.objects.filter(timestamp__month=1, timestamp__year=date.year)
        for order in jan_orders:
            jan_profit += sum(item.profit for item in order.orderItems.all())

        feb_orders = Order.objects.filter(timestamp__month=2, timestamp__year=date.year)
        for order in feb_orders:
            feb_profit += sum(item.profit for item in order.orderItems.all())

        march_orders = Order.objects.filter(timestamp__month=3, timestamp__year=date.year)
        for order in march_orders:
            march_profit += sum(item.profit for item in order.orderItems.all())

        april_orders = Order.objects.filter(timestamp__month=4, timestamp__year=date.year)
        for order in april_orders:
            april_profit += sum(item.profit for item in order.orderItems.all())

        may_orders = Order.objects.filter(timestamp__month=5, timestamp__year=date.year)
        for order in may_orders:
            may_profit += sum(item.profit for item in order.orderItems.all())

        june_orders = Order.objects.filter(timestamp__month=6, timestamp__year=date.year)
        for order in june_orders:
            june_profit += sum(item.profit for item in order.orderItems.all())

        july_orders = Order.objects.filter(timestamp__month=7, timestamp__year=date.year)
        for order in july_orders:
            july_profit += sum(item.profit for item in order.orderItems.all())

        aug_orders = Order.objects.filter(timestamp__month=8, timestamp__year=date.year)
        for order in aug_orders:
            aug_profit += sum(item.profit for item in order.orderItems.all())

        sep_orders = Order.objects.filter(timestamp__month=9, timestamp__year=date.year)
        for order in sep_orders:
            sep_profit += sum(item.profit for item in order.orderItems.all())

        oct_orders = Order.objects.filter(timestamp__month=10, timestamp__year=date.year)
        for order in oct_orders:
            oct_profit += sum(item.profit for item in order.orderItems.all())

        nov_orders = Order.objects.filter(timestamp__month=11, timestamp__year=date.year)
        for order in nov_orders:
            nov_profit += sum(item.profit for item in order.orderItems.all())

        dec_orders = Order.objects.filter(timestamp__month=12, timestamp__year=date.year)
        for order in dec_orders:
            dec_profit += sum(item.profit for item in order.orderItems.all())

        profit_summary.update({
            "January": jan_profit, "February": feb_profit, "March": march_profit,
            "April": april_profit, "May": may_profit, "June": june_profit,
            "July": july_profit, "August": aug_profit, "September": sep_profit,
            "October": oct_profit, "November": nov_profit, "December": dec_profit
        })

        return Response({"data": profit_summary}, status=status.HTTP_200_OK)









