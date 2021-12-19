from .models import Expense
from rest_framework import serializers


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Expense
        fields = "__all__"



class AddExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Expense
        fields = ["expense_type", "expense_amount", "timestamp"]


