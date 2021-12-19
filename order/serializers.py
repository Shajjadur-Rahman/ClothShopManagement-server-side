from rest_framework import serializers
from stock.models import Product
from .models import Customer, Cart, Order


class CustomerSerializer(serializers.ModelSerializer):
    customer_type = serializers.SerializerMethodField("get_customer_type")
    class Meta:
        model  = Customer
        fields = "__all__"

    def get_customer_type(self, obj):
        return obj.get_customer_type_display()



class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Cart
        fields = ["product", "quantity"]


class ProductSerializerForCart(serializers.ModelSerializer):
    class Meta:
        model  = Product
        fields = '__all__'



class ResponseCartSerializer(serializers.ModelSerializer):
    product  = ProductSerializerForCart()
    customer = CustomerSerializer()
    class Meta:
        model  = Cart
        fields = ["customer", "product", "sold_by", "price", "profit", "quantity", "unit_tag", "discount", "sub_total", "timestamp", "updated"]


class CartSerializerForCompleteOrder(serializers.ModelSerializer):
    class Meta:
        model  = Cart
        fields = "__all__"




class OrderSerializer(serializers.ModelSerializer):
    orderItems = ResponseCartSerializer(many=True, read_only=True)

    class Meta:
        model  = Order
        fields = ["id", "order_id", "order_status", "orderItems", "paid_amount", "due_amount", "timestamp"]
        depth  = 1





