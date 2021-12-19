from django.db import models
from django.conf import settings
from stock.models import ImportInvoice
from django.template.defaultfilters import truncatechars

class Expense(models.Model):
    invoice        = models.ForeignKey(ImportInvoice, on_delete=models.SET_NULL, null=True, blank=True)
    expense_type   = models.CharField(max_length=300)
    expense_amount = models.FloatField(default=0.00)
    entry_by       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    creator_name   = models.CharField(max_length=300)
    timestamp      = models.DateTimeField()

    def __str__(self):
        return truncatechars(self.expense_type, 30)
