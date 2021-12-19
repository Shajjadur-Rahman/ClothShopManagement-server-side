from django.db import models
from stock.models import Product
from django.conf import settings
from .utils import unique_order_id_generator
from django.db.models.signals import pre_save




class Customer(models.Model):
    TYPE = (
        ("1", "New"),
        ("2", "Regular"),
    )
    name          = models.CharField(max_length=200)
    customer_type = models.CharField(max_length=20, choices=TYPE, default="1")
    phone         = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class Cart(models.Model):
    customer         = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, related_name='carts')
    product          = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True, related_name='cart_products')
    sold_by          = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='sellers')
    price            = models.FloatField(default=0.00)
    purchasing_price = models.FloatField(default=0.00)
    unit_tag         = models.CharField(max_length=200, null=True, blank=True)
    quantity         = models.FloatField(default=1)
    discount         = models.FloatField(default=0.00)
    sub_total        = models.FloatField(default=0.00)
    profit           = models.FloatField(default=0.00)
    purchased        = models.BooleanField(default=False)
    timestamp        = models.DateTimeField(auto_now_add=True)
    updated          = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.quantity} X {self.product.name}"


    def get_sub_total(self):
        value = 0
        if self.discount:
            value += (self.price * float(self.quantity)) - self.discount
        else:
            value += self.price * self.quantity
        return round(value, 3)


    def save(self, *args, **kwargs):
        print(self.get_sub_total())
        self.sub_total = self.get_sub_total()
        self.profit    = round((self.sub_total - self.purchasing_price * self.quantity), 3)
        super(Cart, self).save(*args, **kwargs)


    def grand_total_imported(self):
        value = self.quantity * self.price
        return round(value, 3)



class OrderManager(models.Manager):  # Custom model manager
    def get_orders(self, customer):
        return super(OrderManager, self).filter(customer=customer)



class Order(models.Model):
    STATUS = (
        ("1", "New"),
        ("2", "Paid"),
        ("3", "Due"),
    )
    orderItems   = models.ManyToManyField(Cart)
    customer     = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order_status = models.CharField(max_length=20, choices=STATUS, default="1")
    paid_amount  = models.FloatField(default=0.00)
    due_amount   = models.FloatField(default=0.00)
    order_id     = models.CharField(max_length=264, blank=True, null=True)
    timestamp    = models.DateTimeField(auto_now_add=True)
    updated      = models.DateTimeField(auto_now=True)
    objects      = OrderManager()

    def __str__(self):
        return str(self.order_id)

    class Meta:
        ordering = ["-pk"]


    def get_totals(self):
        total = 0
        for order_item in self.oderItems.all():
            total += float(order_item.sub_total)
        return round(total, 2)


    def get_total_profit_or_loss(self):
        total = 0
        for order_item in self.orderItems.all():
            total += float(order_item.profit)
        return round(total, 2)

    # def save(self, *args, **kwargs):
    #     self.total_profit += self.get_total_profit()
    #     super(Order, self).save(*args, **kwargs)



def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)



pre_save.connect(pre_save_create_order_id, sender=Order)