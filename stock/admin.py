from django.contrib import admin
from .models import (
    ImportInvoice,
    Company,
    Category,
    Product
)

admin.site.register(ImportInvoice)
admin.site.register(Company)
admin.site.register(Category)
admin.site.register(Product)