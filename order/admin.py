from django.contrib import admin
from .models import Customer, Cart, Order

admin.site.register(Customer)
admin.site.register(Cart)
admin.site.register(Order)
