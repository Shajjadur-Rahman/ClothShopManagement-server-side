from datetime import datetime
from django.utils import timezone
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from account.authentication import Authentication
from rest_framework.permissions import IsAuthenticated
from .models import Customer, Cart, Order
from stock.models import Product
from rest_framework.generics import (
    ListAPIView
)
from .serializers import (
    CustomerSerializer,
    CartSerializer,
    OrderSerializer,
    ResponseCartSerializer,
    CartSerializerForCompleteOrder,
)
from django.db.models import Sum, Case, When, Count
from django.db.models.functions import TruncMonth



class SearchCustomerApiView(ListAPIView):
    authentication_classes = [Authentication]
    permission_classes     = [IsAuthenticated]
    serializer_class       = CustomerSerializer

    def get(self, *args, **kwargs):
        phone = self.request.GET.get("phone")
        if phone:
            try:
                customer = Customer.objects.get(phone=phone)
                serializer = self.serializer_class(customer, many=False)
                return Response(serializer.data)
            except Exception as e:
                return Response({"customer": {}})
        return Response(None)



class AddToCartApiView(APIView):
    authentication_classes = [Authentication]
    permission_classes     = [IsAuthenticated]

    def post(self, *args, **kwargs):

        customer = None
        try:
            product = Product.objects.get(id=self.request.data["product"])
        except Exception as e:
            return Response({"error": "Query does not exist !"})
        customer_id = self.request.data.get("id", None)
        len_qty = self.request.data.get("len_qty", None)
        quantity = self.request.data.get("quantity", None)
        if customer_id is not None:
            pass
        else:
            customer_serializer = CustomerSerializer(data=self.request.data)
            customer_serializer.is_valid(raise_exception=True)
            customer  = customer_serializer.save()
        if customer_id is not None:
            order_item, created = Cart.objects.get_or_create(
                customer_id=customer_id,
                product_id=product.id,
                sold_by=self.request.user,
                unit_tag=self.request.data["unit_tag"],
                purchased=False
            )
        else:
            order_item, created = Cart.objects.get_or_create(
                customer_id=customer.id,
                product_id=product.id,
                sold_by=self.request.user,
                unit_tag=self.request.data["unit_tag"],
                purchased=False
            )
        if customer_id is not None:
            order_qs = Order.objects.filter(customer_id=customer_id, order_status="1")
            carts    = Cart.objects.filter(customer_id=customer_id, purchased=False)
        else:
            order_qs     = Order.objects.filter(customer_id=customer.id, order_status="1")
            carts        = Cart.objects.filter(customer_id=customer.id, purchased=False)
        total_item       = carts.count()
        if order_qs.exists():
            order = order_qs[0]
            if order.orderItems.filter(product_id=product.id).exists():
                if len_qty is not None:
                    order_item.quantity += float(len_qty)
                if quantity is not None:
                    order_item.quantity += int(quantity)
                order_item.price = round(float(self.request.data["price"]), 2)
                order_item.purchasing_price = float(self.request.data["purchasing_price"])
                if self.request.data["discount"]:
                    order_item.discount = round(float(self.request.data["discount"]), 2)
                order_item.save()
                if len_qty is not None:
                    product.len_qty -= float(len_qty)
                if quantity is not None:
                    product.quantity -= float(quantity)
                product.save()
                serializer = ResponseCartSerializer(order_item, many=False)
                return Response({"data": serializer.data, "total_item": total_item}, status=status.HTTP_200_OK)
            else:
                if len_qty is not None:
                    order_item.quantity = float(len_qty)
                if quantity is not None:
                    order_item.quantity = float(quantity)
                order_item.price = round(float(self.request.data["price"]), 2)
                order_item.purchasing_price = round(float(self.request.data["purchasing_price"]), 2)
                if self.request.data["discount"]:
                    order_item.discount = round(float(self.request.data["discount"]), 2)
                order_item.save()
                order.orderItems.add(order_item)
                if len_qty is not None:
                    product.len_qty -= float(len_qty)
                if quantity is not None:
                    product.quantity -= float(quantity)
                product.save()
                serializer = ResponseCartSerializer(order_item, many=False)
                return Response({"data": serializer.data, "total_item": total_item}, status=status.HTTP_200_OK)

        if customer_id is not None:
            order = Order.objects.create(customer_id=customer_id)
        else:
            order = Order.objects.create(customer_id=customer.id)

        if len_qty is not None:
            order_item.quantity = float(len_qty)
        if quantity is not None:
            order_item.quantity = float(quantity)
        order_item.price=float(self.request.data["price"])
        order_item.purchasing_price = round(float(self.request.data["purchasing_price"]), 2)
        if self.request.data["discount"]:
            order_item.discount = round(float(self.request.data["discount"]), 2)
        order_item.save()
        order.orderItems.add(order_item)
        if len_qty is not None:
            product.len_qty -= float(len_qty)
        if quantity is not None:
            product.quantity -= float(quantity)
        product.save()
        serializer = ResponseCartSerializer(order_item, many=False)
        return Response({"data": serializer.data, "total_item": total_item}, status=status.HTTP_200_OK)



class RemoveProductApiView(APIView):
    authentication_classes = [Authentication]
    permission_classes     = [IsAuthenticated]

    def post(self, *args, **kwargs):
        try:
            product = Product.objects.get(id=kwargs["product_id"])
        except Exception as e:
            product = None
        order_qs = Order.objects.filter(order_status="1", customer_id=kwargs["customer_id"])
        if order_qs.exists():
            order = order_qs[0]
            if order.orderItems.filter(product_id=product.id, purchased=False).exists():
                ordered_item = Cart.objects.filter(
                    customer_id=kwargs["customer_id"],
                    product_id=product.id,
                    purchased=False,
                )[0]
                if kwargs["type"] == "fabric":
                    product.len_qty += float(kwargs["p_qty"])
                if  kwargs["type"] == "not_fabric":
                    product.quantity += float(kwargs["p_qty"])
                product.save()
                order.orderItems.remove(ordered_item)
                ordered_item.delete()
                if order.orderItems.filter(customer_id=kwargs["customer_id"], purchased=False).exists():
                    pass
                else:
                    order.delete()
                return Response({"success": "Product removed from cart !"}, status=status.HTTP_200_OK)
            return Response({"error": "Product not fount in your cart !"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"error": "Not active order for this customer !"}, status=status.HTTP_404_NOT_FOUND)







class CartApiView(ListAPIView):
    authentication_classes = [Authentication]
    permission_classes     = [IsAuthenticated]
    serializer_class       = ResponseCartSerializer

    def get(self, *args, **kwargs):
        cart_items       = Cart.objects.filter(customer_id=kwargs["id"], purchased=False)
        total_cart_items = Cart.objects.filter(customer_id=kwargs["id"], purchased=False).count()
        total            = sum(item.sub_total for item in cart_items)
        total_discount            = sum(item.discount for item in cart_items)
        serializer = self.serializer_class(cart_items, context={'request': self.request}, many=True)
        return Response({"data": serializer.data,
                         "total_cart_items": total_cart_items,
                         "total": total,
                         "total_discount": total_discount}, status=status.HTTP_200_OK)



class CompleteOrderApiView(APIView):
    authentication_classes = [Authentication]
    permission_classes     = [IsAuthenticated]

    def post(self, *args, **kwargs):
        paid_amount = kwargs["paid_amount"]
        total = sum(item.sub_total for item in Cart.objects.filter(customer_id=kwargs["id"], purchased=False))
        if float(total) == float(paid_amount):
            Cart.objects.filter(customer_id=kwargs["id"], purchased=False).update(purchased=True)
            order = Order.objects.get(customer_id=kwargs["id"], order_status="1")
            order.order_status = "2"
            order.paid_amount  = float(paid_amount)
            order.due_amount  = float(total) - float(paid_amount)
            order.save()
            return Response({"success": "Order completed !"}, status=status.HTTP_200_OK)
        elif float(total) > float(paid_amount):
            Cart.objects.filter(customer_id=kwargs["id"], purchased=False).update(purchased=True)
            order = Order.objects.get(customer_id=kwargs["id"], order_status="1")
            order.order_status = "3"
            order.paid_amount  = float(paid_amount)
            order.due_amount  = float(total) - float(paid_amount)
            order.save()
            return Response({"success": "Order completed !"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid paid amount !"})




from itertools import groupby
class OrderInYearApiView(APIView):
    authentication_classes = [Authentication]
    permission_classes     = [IsAuthenticated]
    serializer_class       = OrderSerializer

    def get_month(self, timestamp):
        month = timestamp.month
        return month

    def get_year(self, timestamp):
        year = timestamp.year
        return year

    def get(self, *args, **kwargs):
        date                 = datetime.now()
        year                 = self.request.GET.get("year")
        jan_p_price   = 0
        jan_sold_qty  = 0
        jan_sub_total = 0
        jan_discount  = 0
        jan_profit    = 0

        feb_p_price   = 0
        feb_sold_qty  = 0
        feb_sub_total = 0
        feb_discount  = 0
        feb_profit    = 0

        march_p_price   = 0
        march_sold_qty  = 0
        march_sub_total = 0
        march_discount  = 0
        march_profit    = 0

        april_p_price   = 0
        april_sold_qty  = 0
        april_sub_total = 0
        april_discount  = 0
        april_profit    = 0

        may_p_price   = 0
        may_sold_qty  = 0
        may_sub_total = 0
        may_discount  = 0
        may_profit    = 0

        june_p_price   = 0
        june_sold_qty  = 0
        june_sub_total = 0
        june_discount  = 0
        june_profit    = 0

        july_p_price   = 0
        july_sold_qty  = 0
        july_sub_total = 0
        july_discount  = 0
        july_profit    = 0

        aug_p_price   = 0
        aug_sold_qty  = 0
        aug_sub_total = 0
        aug_discount  = 0
        aug_profit    = 0

        sep_p_price   = 0
        sep_sold_qty  = 0
        sep_sub_total = 0
        sep_discount  = 0
        sep_profit    = 0

        oct_p_price   = 0
        oct_sold_qty  = 0
        oct_sub_total = 0
        oct_discount  = 0
        oct_profit    = 0

        nov_p_price   = 0
        nov_sold_qty  = 0
        nov_sub_total = 0
        nov_discount  = 0
        nov_profit    = 0

        dec_p_price   = 0
        dec_sold_qty  = 0
        dec_sub_total = 0
        dec_discount  = 0
        dec_profit    = 0

        sold_qty_in_year = 0

        if year:
            orders_in_year       = Order.objects.filter(timestamp__year=year)
            total_profit_in_year = sum(order.get_total_profit_or_loss() for order in orders_in_year)
            for order in orders_in_year:
                sold_qty_in_year += sum(item.quantity for item in order.orderItems.all())

            jan_orders         = Order.objects.filter(timestamp__month=1, timestamp__year=year)
            for order in jan_orders:
                jan_p_price   += sum(item.purchasing_price for item in order.orderItems.all())
                jan_sold_qty  += sum(item.quantity for item in order.orderItems.all())
                jan_sub_total += sum(item.sub_total for item in order.orderItems.all())
                jan_discount  += sum(item.discount for item in order.orderItems.all())
                jan_profit    += sum(item.profit for item in order.orderItems.all())

            feb_orders         = Order.objects.filter(timestamp__month=2, timestamp__year=year)
            for order in feb_orders:
                feb_p_price   += sum(item.purchasing_price for item in order.orderItems.all())
                feb_sold_qty  += sum(item.quantity for item in order.orderItems.all())
                feb_sub_total += sum(item.sub_total for item in order.orderItems.all())
                feb_discount  += sum(item.discount for item in order.orderItems.all())
                feb_profit    += sum(item.profit for item in order.orderItems.all())

            march_orders         = Order.objects.filter(timestamp__month=3, timestamp__year=year)
            for order in march_orders:
                march_p_price   += sum(item.purchasing_price for item in order.orderItems.all())
                march_sold_qty  += sum(item.quantity for item in order.orderItems.all())
                march_sub_total += sum(item.sub_total for item in order.orderItems.all())
                march_discount  += sum(item.discount for item in order.orderItems.all())
                march_profit    += sum(item.profit for item in order.orderItems.all())

            april_orders         = Order.objects.filter(timestamp__month=4, timestamp__year=year)
            for order in april_orders:
                april_p_price   += sum(item.purchasing_price for item in order.orderItems.all())
                april_sold_qty  += sum(item.quantity for item in order.orderItems.all())
                april_sub_total += sum(item.sub_total for item in order.orderItems.all())
                april_discount  += sum(item.discount for item in order.orderItems.all())
                april_profit    += sum(item.profit for item in order.orderItems.all())

            may_orders         = Order.objects.filter(timestamp__month=5, timestamp__year=year)
            for order in may_orders:
                may_p_price   += sum(item.purchasing_price for item in order.orderItems.all())
                may_sold_qty  += sum(item.quantity for item in order.orderItems.all())
                may_sub_total += sum(item.sub_total for item in order.orderItems.all())
                may_discount  += sum(item.discount for item in order.orderItems.all())
                may_profit    += sum(item.profit for item in order.orderItems.all())

            june_orders         = Order.objects.filter(timestamp__month=6, timestamp__year=year)
            for order in june_orders:
                june_p_price   += sum(item.purchasing_price for item in order.orderItems.all())
                june_sold_qty  += sum(item.quantity for item in order.orderItems.all())
                june_sub_total += sum(item.sub_total for item in order.orderItems.all())
                june_discount  += sum(item.discount for item in order.orderItems.all())
                june_profit    += sum(item.profit for item in order.orderItems.all())

            july_orders         = Order.objects.filter(timestamp__month=7, timestamp__year=year)
            for order in july_orders:
                july_p_price   += sum(item.purchasing_price for item in order.orderItems.all())
                july_sold_qty  += sum(item.quantity for item in order.orderItems.all())
                july_sub_total += sum(item.sub_total for item in order.orderItems.all())
                july_discount  += sum(item.discount for item in order.orderItems.all())
                july_profit    += sum(item.profit for item in order.orderItems.all())

            aug_orders         = Order.objects.filter(timestamp__month=8, timestamp__year=year)
            for order in aug_orders:
                aug_p_price   += sum(item.purchasing_price for item in order.orderItems.all())
                aug_sold_qty  += sum(item.quantity for item in order.orderItems.all())
                aug_sub_total += sum(item.sub_total for item in order.orderItems.all())
                aug_discount  += sum(item.discount for item in order.orderItems.all())
                aug_profit    += sum(item.profit for item in order.orderItems.all())

            sep_orders         = Order.objects.filter(timestamp__month=9, timestamp__year=year)
            for order in sep_orders:
                sep_p_price   += sum(item.purchasing_price for item in order.orderItems.all())
                sep_sold_qty  += sum(item.quantity for item in order.orderItems.all())
                sep_sub_total += sum(item.sub_total for item in order.orderItems.all())
                sep_discount  += sum(item.discount for item in order.orderItems.all())
                sep_profit    += sum(item.profit for item in order.orderItems.all())

            oct_orders         = Order.objects.filter(timestamp__month=10, timestamp__year=year)
            for order in oct_orders:
                oct_p_price   += sum(item.purchasing_price for item in order.orderItems.all())
                oct_sold_qty  += sum(item.quantity for item in order.orderItems.all())
                oct_sub_total += sum(item.sub_total for item in order.orderItems.all())
                oct_discount  += sum(item.discount for item in order.orderItems.all())
                oct_profit    += sum(item.profit for item in order.orderItems.all())

            nov_orders         = Order.objects.filter(timestamp__month=11, timestamp__year=year)
            for order in nov_orders:
                nov_p_price   += sum(item.purchasing_price for item in order.orderItems.all())
                nov_sold_qty  += sum(item.quantity for item in order.orderItems.all())
                nov_sub_total += sum(item.sub_total for item in order.orderItems.all())
                nov_discount  += sum(item.discount for item in order.orderItems.all())
                nov_profit    += sum(item.profit for item in order.orderItems.all())

            dec_orders         = Order.objects.filter(timestamp__month=12, timestamp__year=year)
            for order in dec_orders:
                dec_p_price   += sum(item.purchasing_price for item in order.orderItems.all())
                dec_sold_qty  += sum(item.quantity for item in order.orderItems.all())
                dec_sub_total += sum(item.sub_total for item in order.orderItems.all())
                dec_discount  += sum(item.discount for item in order.orderItems.all())
                dec_profit    += sum(item.profit for item in order.orderItems.all())

            order_summary = [
                {"month": "January", "year": date.year, "sold_qty": jan_sold_qty, "purchasing_price": jan_p_price,
                 "discount": jan_discount, "sub_total": jan_sub_total, "profit": jan_profit},
                {"month": "February", "year": date.year, "sold_qty": feb_sold_qty, "purchasing_price": feb_p_price,
                 "discount": feb_discount, "sub_total": feb_sub_total, "profit": feb_profit},
                {"month": "March", "year": date.year, "sold_qty": march_sold_qty, "purchasing_price": march_p_price,
                 "discount": march_discount, "sub_total": march_sub_total, "profit": march_profit},
                {"month": "April", "year": date.year, "sold_qty": april_sold_qty, "purchasing_price": april_p_price,
                 "discount": april_discount, "sub_total": april_sub_total, "profit": april_profit},
                {"month": "May", "year": date.year, "sold_qty": may_sold_qty, "purchasing_price": may_p_price,
                 "discount": may_discount, "sub_total": may_sub_total, "profit": may_profit},
                {"month": "June", "year": date.year, "sold_qty": june_sold_qty, "purchasing_price": june_p_price,
                 "discount": june_discount, "sub_total": june_sub_total, "profit": june_profit},
                {"month": "July", "year": date.year, "sold_qty": july_sold_qty, "purchasing_price": july_p_price,
                 "discount": july_discount, "sub_total": july_sub_total, "profit": july_profit},
                {"month": "August", "year": date.year, "sold_qty": aug_sold_qty, "purchasing_price": aug_p_price,
                 "discount": aug_discount, "sub_total": aug_sub_total, "profit": aug_profit},
                {"month": "September", "year": date.year, "sold_qty": sep_sold_qty, "purchasing_price": sep_p_price,
                 "discount": sep_discount, "sub_total": sep_sub_total, "profit": sep_profit},
                {"month": "October", "year": date.year, "sold_qty": oct_sold_qty, "purchasing_price": oct_p_price,
                 "discount": oct_discount, "sub_total": oct_sub_total, "profit": oct_profit},
                {"month": "November", "year": date.year, "sold_qty": nov_sold_qty, "purchasing_price": nov_p_price,
                 "discount": nov_discount, "sub_total": nov_sub_total, "profit": nov_profit},
                {"month": "December", "year": date.year, "sold_qty": dec_sold_qty, "purchasing_price": dec_p_price,
                 "discount": dec_discount, "sub_total": dec_sub_total, "profit": dec_profit},
            ]
            return Response({"order_summary": order_summary, "total_profit_in_year": total_profit_in_year,
                             "sold_qty_in_year": sold_qty_in_year, "year": year}, status=status.HTTP_200_OK)

        orders_in_year       = Order.objects.filter(timestamp__year=date.year)
        total_profit_in_year = sum(order.get_total_profit_or_loss() for order in orders_in_year)
        for order in orders_in_year:
            sold_qty_in_year += sum(item.quantity for item in order.orderItems.all())

        jan_orders         = Order.objects.filter(timestamp__month=1, timestamp__year=date.year)
        for order in jan_orders:
            jan_p_price   += sum(item.purchasing_price for item in order.orderItems.all())
            jan_sold_qty  += sum(item.quantity for item in order.orderItems.all())
            jan_sub_total += sum(item.sub_total for item in order.orderItems.all())
            jan_discount  += sum(item.discount for item in order.orderItems.all())
            jan_profit    += sum(item.profit for item in order.orderItems.all())

        feb_orders         = Order.objects.filter(timestamp__month=2, timestamp__year=date.year)
        for order in feb_orders:
            feb_p_price   += sum(item.purchasing_price for item in order.orderItems.all())
            feb_sold_qty  += sum(item.quantity for item in order.orderItems.all())
            feb_sub_total += sum(item.sub_total for item in order.orderItems.all())
            feb_discount  += sum(item.discount for item in order.orderItems.all())
            feb_profit    += sum(item.profit for item in order.orderItems.all())

        march_orders         = Order.objects.filter(timestamp__month=3, timestamp__year=date.year)
        for order in march_orders:
            march_p_price   += sum(item.purchasing_price for item in order.orderItems.all())
            march_sold_qty  += sum(item.quantity for item in order.orderItems.all())
            march_sub_total += sum(item.sub_total for item in order.orderItems.all())
            march_discount  += sum(item.discount for item in order.orderItems.all())
            march_profit    += sum(item.profit for item in order.orderItems.all())

        april_orders        = Order.objects.filter(timestamp__month=4, timestamp__year=date.year)
        for order in april_orders:
            april_p_price   += sum(item.purchasing_price for item in order.orderItems.all())
            april_sold_qty  += sum(item.quantity for item in order.orderItems.all())
            april_sub_total += sum(item.sub_total for item in order.orderItems.all())
            april_discount  += sum(item.discount for item in order.orderItems.all())
            april_profit    += sum(item.profit for item in order.orderItems.all())

        may_orders         = Order.objects.filter(timestamp__month=5, timestamp__year=date.year)
        for order in may_orders:
            may_p_price   += sum(item.purchasing_price for item in order.orderItems.all())
            may_sold_qty  += sum(item.quantity for item in order.orderItems.all())
            may_sub_total += sum(item.sub_total for item in order.orderItems.all())
            may_discount  += sum(item.discount for item in order.orderItems.all())
            may_profit    += sum(item.profit for item in order.orderItems.all())

        june_orders         = Order.objects.filter(timestamp__month=6, timestamp__year=date.year)
        for order in june_orders:
            june_p_price   += sum(item.purchasing_price for item in order.orderItems.all())
            june_sold_qty  += sum(item.quantity for item in order.orderItems.all())
            june_sub_total += sum(item.sub_total for item in order.orderItems.all())
            june_discount  += sum(item.discount for item in order.orderItems.all())
            june_profit    += sum(item.profit for item in order.orderItems.all())

        july_orders         = Order.objects.filter(timestamp__month=7, timestamp__year=date.year)
        for order in july_orders:
            july_p_price   += sum(item.purchasing_price for item in order.orderItems.all())
            july_sold_qty  += sum(item.quantity for item in order.orderItems.all())
            july_sub_total += sum(item.sub_total for item in order.orderItems.all())
            july_discount  += sum(item.discount for item in order.orderItems.all())
            july_profit    += sum(item.profit for item in order.orderItems.all())

        aug_orders         = Order.objects.filter(timestamp__month=8, timestamp__year=date.year)
        for order in aug_orders:
            aug_p_price   += sum(item.purchasing_price for item in order.orderItems.all())
            aug_sold_qty  += sum(item.quantity for item in order.orderItems.all())
            aug_sub_total += sum(item.sub_total for item in order.orderItems.all())
            aug_discount  += sum(item.discount for item in order.orderItems.all())
            aug_profit    += sum(item.profit for item in order.orderItems.all())

        sep_orders         = Order.objects.filter(timestamp__month=9, timestamp__year=date.year)
        for order in sep_orders:
            sep_p_price   += sum(item.purchasing_price for item in order.orderItems.all())
            sep_sold_qty  += sum(item.quantity for item in order.orderItems.all())
            sep_sub_total += sum(item.sub_total for item in order.orderItems.all())
            sep_discount  += sum(item.discount for item in order.orderItems.all())
            sep_profit    += sum(item.profit for item in order.orderItems.all())

        oct_orders         = Order.objects.filter(timestamp__month=10, timestamp__year=date.year)
        for order in oct_orders:
            oct_p_price   += sum(item.purchasing_price for item in order.orderItems.all())
            oct_sold_qty  += sum(item.quantity for item in order.orderItems.all())
            oct_sub_total += sum(item.sub_total for item in order.orderItems.all())
            oct_discount  += sum(item.discount for item in order.orderItems.all())
            oct_profit    += sum(item.profit for item in order.orderItems.all())

        nov_orders         = Order.objects.filter(timestamp__month=11, timestamp__year=date.year)
        for order in nov_orders:
            nov_p_price   += sum(item.purchasing_price for item in order.orderItems.all())
            nov_sold_qty  += sum(item.quantity for item in order.orderItems.all())
            nov_sub_total += sum(item.sub_total for item in order.orderItems.all())
            nov_discount  += sum(item.discount for item in order.orderItems.all())
            nov_profit    += sum(item.profit for item in order.orderItems.all())

        dec_orders         = Order.objects.filter(timestamp__month=12, timestamp__year=date.year)
        for order in dec_orders:
            dec_p_price   += sum(item.purchasing_price for item in order.orderItems.all())
            dec_sold_qty  += sum(item.quantity for item in order.orderItems.all())
            dec_sub_total += sum(item.sub_total for item in order.orderItems.all())
            dec_discount  += sum(item.discount for item in order.orderItems.all())
            dec_profit    += sum(item.profit for item in order.orderItems.all())

        order_summary = [
            {"month": "January", "year": date.year, "sold_qty": jan_sold_qty, "purchasing_price": jan_p_price,
             "discount": jan_discount, "sub_total": jan_sub_total, "profit": jan_profit},
            {"month": "February", "year": date.year, "sold_qty": feb_sold_qty, "purchasing_price": feb_p_price,
             "discount": feb_discount, "sub_total": feb_sub_total, "profit": feb_profit},
            {"month": "March", "year": date.year, "sold_qty": march_sold_qty, "purchasing_price": march_p_price,
             "discount": march_discount, "sub_total": march_sub_total, "profit": march_profit},
            {"month": "April", "year": date.year, "sold_qty": april_sold_qty, "purchasing_price": april_p_price,
             "discount": april_discount, "sub_total": april_sub_total, "profit": april_profit},
            {"month": "May", "year": date.year, "sold_qty": may_sold_qty, "purchasing_price": may_p_price,
             "discount": may_discount, "sub_total": may_sub_total, "profit": may_profit},
            {"month": "June", "year": date.year, "sold_qty": june_sold_qty, "purchasing_price": june_p_price,
             "discount": june_discount, "sub_total": june_sub_total, "profit": june_profit},
            {"month": "July", "year": date.year, "sold_qty": july_sold_qty, "purchasing_price": july_p_price,
             "discount": july_discount, "sub_total": july_sub_total, "profit": july_profit},
            {"month": "August", "year": date.year, "sold_qty": aug_sold_qty, "purchasing_price": aug_p_price,
             "discount": aug_discount, "sub_total": aug_sub_total, "profit": aug_profit},
            {"month": "September", "year": date.year, "sold_qty": sep_sold_qty, "purchasing_price": sep_p_price,
             "discount": sep_discount, "sub_total": sep_sub_total, "profit": sep_profit},
            {"month": "October", "year": date.year, "sold_qty": oct_sold_qty, "purchasing_price": oct_p_price,
             "discount": oct_discount, "sub_total": oct_sub_total, "profit": oct_profit},
            {"month": "November", "year": date.year, "sold_qty": nov_sold_qty, "purchasing_price": nov_p_price,
             "discount": nov_discount, "sub_total": nov_sub_total, "profit": nov_profit},
            {"month": "December", "year": date.year, "sold_qty": dec_sold_qty, "purchasing_price": dec_p_price,
             "discount": dec_discount, "sub_total": dec_sub_total, "profit": dec_profit},
        ]
        return Response({"order_summary": order_summary, "total_profit_in_year": total_profit_in_year,
                         "sold_qty_in_year": sold_qty_in_year, "year": date.year}, status=status.HTTP_200_OK)



# Sales analytics
class SaleAnalyticApiView(APIView):
    authentication_classes = [Authentication]
    permission_classes     = [IsAuthenticated]

    def get(self, *args, **kwargs):
        date = datetime.now()
        jan_sub_total   = 0
        feb_sub_total   = 0
        march_sub_total = 0
        april_sub_total = 0
        may_sub_total   = 0
        june_sub_total  = 0
        july_sub_total  = 0
        aug_sub_total   = 0
        sep_sub_total   = 0
        oct_sub_total   = 0
        nov_sub_total   = 0
        dec_sub_total   = 0

        sales_summary = {}

        jan_orders         = Order.objects.filter(timestamp__month=1, timestamp__year=date.year)
        for order in jan_orders:
            jan_sub_total += sum(item.sub_total for item in order.orderItems.all())

        feb_orders         = Order.objects.filter(timestamp__month=2, timestamp__year=date.year)
        for order in feb_orders:
            feb_sub_total += sum(item.sub_total for item in order.orderItems.all())

        march_orders         = Order.objects.filter(timestamp__month=3, timestamp__year=date.year)
        for order in march_orders:
            march_sub_total += sum(item.sub_total for item in order.orderItems.all())

        april_orders        = Order.objects.filter(timestamp__month=4, timestamp__year=date.year)
        for order in april_orders:
            april_sub_total += sum(item.sub_total for item in order.orderItems.all())

        may_orders         = Order.objects.filter(timestamp__month=5, timestamp__year=date.year)
        for order in may_orders:
            may_sub_total += sum(item.sub_total for item in order.orderItems.all())

        june_orders         = Order.objects.filter(timestamp__month=6, timestamp__year=date.year)
        for order in june_orders:
            june_sub_total += sum(item.sub_total for item in order.orderItems.all())

        july_orders         = Order.objects.filter(timestamp__month=7, timestamp__year=date.year)
        for order in july_orders:
            july_sub_total += sum(item.sub_total for item in order.orderItems.all())

        aug_orders         = Order.objects.filter(timestamp__month=8, timestamp__year=date.year)
        for order in aug_orders:
            aug_sub_total += sum(item.sub_total for item in order.orderItems.all())

        sep_orders         = Order.objects.filter(timestamp__month=9, timestamp__year=date.year)
        for order in sep_orders:
            sep_sub_total += sum(item.sub_total for item in order.orderItems.all())

        oct_orders         = Order.objects.filter(timestamp__month=10, timestamp__year=date.year)
        for order in oct_orders:
            oct_sub_total += sum(item.sub_total for item in order.orderItems.all())

        nov_orders         = Order.objects.filter(timestamp__month=11, timestamp__year=date.year)
        for order in nov_orders:
            nov_sub_total += sum(item.sub_total for item in order.orderItems.all())

        dec_orders         = Order.objects.filter(timestamp__month=12, timestamp__year=date.year)
        for order in dec_orders:
            dec_sub_total += sum(item.sub_total for item in order.orderItems.all())

        sales_summary.update({
            "January": jan_sub_total, "February": feb_sub_total, "March": march_sub_total,
            "April": april_sub_total, "May": may_sub_total, "June": june_sub_total,
            "July": july_sub_total, "August": aug_sub_total, "September": sep_sub_total,
            "October": oct_sub_total, "November": nov_sub_total, "December": dec_sub_total
        })
        return Response({"data": sales_summary}, status=status.HTTP_200_OK)


# Due sale analytics
class DueSaleAnalyticApiView(APIView):
    authentication_classes = [Authentication]
    permission_classes     = [IsAuthenticated]

    def get(self, *args, **kwargs):
        date = datetime.now()
        jan_due_order_amount   = 0
        feb_due_order_amount   = 0
        march_due_order_amount = 0
        april_due_order_amount = 0
        may_due_order_amount   = 0
        june_due_order_amount  = 0
        july_due_order_amount  = 0
        aug_due_order_amount   = 0
        sep_due_order_amount   = 0
        oct_due_order_amount   = 0
        nov_due_order_amount   = 0
        dec_due_order_amount   = 0

        due_sales_summary = {}

        jan_orders            = Order.objects.filter(timestamp__month=1, timestamp__year=date.year, order_status="3")
        jan_due_order_amount += sum(order.due_amount for order in jan_orders)

        feb_orders            = Order.objects.filter(timestamp__month=2, timestamp__year=date.year, order_status="3")
        feb_due_order_amount += sum(order.due_amount for order in feb_orders)

        march_orders            = Order.objects.filter(timestamp__month=3, timestamp__year=date.year, order_status="3")
        march_due_order_amount += sum(order.due_amount for order in march_orders)

        april_orders            = Order.objects.filter(timestamp__month=4, timestamp__year=date.year, order_status="3")
        april_due_order_amount += sum(order.due_amount for order in april_orders)

        may_orders            = Order.objects.filter(timestamp__month=5, timestamp__year=date.year, order_status="3")
        may_due_order_amount += sum(order.due_amount for order in may_orders)

        june_orders            = Order.objects.filter(timestamp__month=6, timestamp__year=date.year, order_status="3")
        june_due_order_amount += sum(order.due_amount for order in june_orders)

        july_orders            = Order.objects.filter(timestamp__month=7, timestamp__year=date.year, order_status="3")
        july_due_order_amount += sum(order.due_amount for order in july_orders)

        aug_orders            = Order.objects.filter(timestamp__month=8, timestamp__year=date.year, order_status="3")
        aug_due_order_amount += sum(order.due_amount for order in aug_orders)

        sep_orders            = Order.objects.filter(timestamp__month=9, timestamp__year=date.year, order_status="3")
        sep_due_order_amount += sum(order.due_amount for order in sep_orders)

        oct_orders            = Order.objects.filter(timestamp__month=10, timestamp__year=date.year, order_status="3")
        oct_due_order_amount += sum(order.due_amount for order in oct_orders)

        nov_orders            = Order.objects.filter(timestamp__month=11, timestamp__year=date.year, order_status="3")
        nov_due_order_amount += sum(order.due_amount for order in nov_orders)

        dec_orders            = Order.objects.filter(timestamp__month=12, timestamp__year=date.year, order_status="3")
        dec_due_order_amount += sum(order.due_amount for order in dec_orders)

        due_sales_summary.update({
            "January": july_due_order_amount, "February": feb_due_order_amount, "March": march_due_order_amount,
            "April": april_due_order_amount, "May": may_due_order_amount, "June": june_due_order_amount,
            "July": july_due_order_amount, "August": aug_due_order_amount, "September": sep_due_order_amount,
            "October": oct_due_order_amount, "November": nov_due_order_amount, "December": dec_due_order_amount
        })
        return Response({"data": due_sales_summary}, status=status.HTTP_200_OK)



class TotalOrderSummaryApiView(APIView):
    authentication_classes = [Authentication]
    permission_classes     = [IsAuthenticated]

    def get(self, *args, **kwargs):
        date               = datetime.now()
        today_total_sale   = 0
        today_due_sale     = 0
        today_cash_sale    = 0
        current_month_sale = 0
        order_summary      = {}

        today_orders       = Order.objects.filter(timestamp__year=date.year, timestamp__month=date.month, timestamp__day=date.day)
        today_due_sale    += sum(order.due_amount for order in today_orders.all())
        today_cash_sale   += sum(order.paid_amount for order in today_orders.all())
        for order in today_orders:
            today_total_sale += sum(item.sub_total for item in order.orderItems.all())
        current_month_sale += sum(item.sub_total for item in Cart.objects.filter(timestamp__month=date.month, timestamp__year=date.year))
        order_summary.update({
           "today_total_sale": today_total_sale, "today_due_sale": today_due_sale, "today_cash_sale": today_cash_sale,
            "current_month_sale": current_month_sale
        })

        return Response({"data": order_summary}, status=status.HTTP_200_OK)





class SaleInMonthApiView(APIView):
    authentication_classes = [Authentication]
    permission_classes     = [IsAuthenticated]
    serializer_class       = ResponseCartSerializer


    def get(self, *args, **kwargs):
        requested_month = str(kwargs['month'])
        month_obj       = datetime.strptime(requested_month, "%B")
        get_moth        = month_obj.month
        sales           = Cart.objects.filter(timestamp__month=get_moth, timestamp__year=kwargs['year'])
        total_sales     = sum(item.sub_total for item in sales)
        total_qty       = sum(item.quantity for item in sales)
        total_profit    = sum(item.profit for item in sales)
        serializer = self.serializer_class(sales, many=True)
        return Response({"data": serializer.data, "total_sales": round(total_sales, 3), "total_qty": round(total_qty, 3),
                         "total_profit": round(total_profit, 3)}, status=status.HTTP_200_OK)



class TodaySaleApiView(APIView):
    authentication_classes = [Authentication]
    permission_classes     = [IsAuthenticated]
    serializer_class       = ResponseCartSerializer
    
    def get(self, *args, **kwargs):
        date = datetime.now()
        sales           = Cart.objects.filter(timestamp__year=date.year, timestamp__month=date.month,
                                              timestamp__day=date.day)
        total_sales     = sum(item.sub_total for item in sales)
        total_qty       = sum(item.quantity for item in sales)
        total_profit    = sum(item.profit for item in sales)
        serializer = ResponseCartSerializer(sales, many=True)
        return Response({"data": serializer.data, "total_sales": round(total_sales, 3), "total_qty": round(total_qty, 3),
                         "total_profit": round(total_profit, 3)}, status=status.HTTP_200_OK)

    




class ClientsApiView(APIView):
    authentication_classes = [Authentication]
    permission_classes     = [IsAuthenticated]
    serializer_class       = CustomerSerializer

    def get(self, *args, **kwargs):
        phone          = self.request.GET.get('phone', None)
        if phone is not None:
            customers = Customer.objects.filter(phone=phone)
            total_customer = customers.count()
            serializer = self.serializer_class(customers, many=True)
            return Response({"data": serializer.data, "total_customer": total_customer}, status=status.HTTP_200_OK)
        customers      = Customer.objects.all()
        total_customer = customers.count()
        serializer     = self.serializer_class(customers, many=True)
        return Response({"data": serializer.data, "total_customer": total_customer}, status=status.HTTP_200_OK)



class AllOrderApiView(APIView):
    authentication_classes = [Authentication]
    permission_classes     = [IsAuthenticated]
    serializer_class       = OrderSerializer

    def get(self, *args, **kwargs):
        customer_id = kwargs["customer_id"]
        query    = self.request.GET.get("timestamp")
        if query:
            year     = int(query[0:4])
            month    = int(query[5:7])
            day      = int(query[8:12])
            order_qs = Order.objects.filter(customer_id=customer_id, timestamp__year=year,
                                            timestamp__month=month, timestamp__day=day+1)
            serializer = self.serializer_class(order_qs, many=True)
            return Response(serializer.data)
        else:
            order_qs    = Order.objects.get_orders(customer=customer_id) # get_orders method came from model manager !
            serializer  = self.serializer_class(order_qs, many=True)
            return Response(serializer.data)



class DueOrderApiView(APIView):
    authentication_classes = [Authentication]
    permission_classes     = [IsAuthenticated]
    serializer_class       = OrderSerializer

    def get(self, *args, **kwargs):
        customer_id = kwargs["customer_id"]
        query    = self.request.GET.get("timestamp")
        if query:
            year     = int(query[0:4])
            month    = int(query[5:7])
            day      = int(query[8:12])
            order_qs = Order.objects.filter(customer_id=customer_id, order_status="3",
                                            timestamp__year=year, timestamp__month=month, timestamp__day=day+1)
            serializer = self.serializer_class(order_qs, many=True)
            return Response(serializer.data)
        else:
            order_qs    = Order.objects.filter(customer_id=customer_id, order_status="3")
            serializer  = self.serializer_class(order_qs, many=True)
            return Response(serializer.data)



class PayDueAmountApiView(APIView):
    authentication_classes = [Authentication]
    permission_classes     = [IsAuthenticated]

    def post(self, *args, **kwargs):
        paid_amount = kwargs["paid_amount"]
        order_id = kwargs["order_id"]
        try:
            order = Order.objects.get(id=order_id, order_status="3")
        except Exception as e:
            return Response({'data': 'No data fount'}, status=status.HTTP_200_OK)
        if float(paid_amount) and float(paid_amount) <= order.due_amount:
            if float(paid_amount) == order.due_amount:
                order.paid_amount  = order.paid_amount + float(paid_amount)
                order.due_amount   = order.due_amount - float(paid_amount)
                order.order_status = "2"
                order.save()
                return Response({"success": 'Payment completed ! No due '})
            order.paid_amount = order.paid_amount + float(paid_amount)
            order.due_amount = order.due_amount - float(paid_amount)
            order.order_status = "3"
            order.save()
            return Response({"success": 'Payment completed ! No due '})




class TodayDueSalesApiView(APIView):
    authentication_classes = [Authentication]
    permission_classes     = [IsAuthenticated]
    serializer_class       = OrderSerializer

    def get(self, *args, **kwargs):
        date       = datetime.now()
        orders     = Order.objects.filter(timestamp__day=date.day, timestamp__month=date.month,
                                          timestamp__year=date.year, order_status="3")
        total_paid = sum(order.paid_amount for order in orders)
        total_due  = sum(order.due_amount for order in orders)
        total      = total_paid + total_due
        serializer = self.serializer_class(orders, many=True)
        return Response({"data": serializer.data, "total_paid": total_paid, "total_due": total_due, "total": total},
                        status=status.HTTP_200_OK)


class TodayDueSaleItemsApiView(APIView):
    authentication_classes = [Authentication]
    permission_classes     = [IsAuthenticated]

    def get(self, *args, **kwargs):
        order_id   = kwargs["order_id"]
        order      = Order.objects.get(id=order_id, order_status="3")
        items      = order.orderItems.all()
        total_sales = sum(item.sub_total for item in items)
        total_qty = sum(item.quantity for item in items)
        total_profit = sum(item.profit for item in items)
        paid_amount  = order.paid_amount
        due_amount   = order.due_amount
        serializer = ResponseCartSerializer(items, many=True)
        return Response({"data": serializer.data, "total_sales": total_sales, "total_qty": total_qty,
                         "total_profit": total_profit, "paid_amount": paid_amount,
                         "due_amount": due_amount}, status=status.HTTP_200_OK)




class TodayCashSalesApiView(APIView):
    authentication_classes = [Authentication]
    permission_classes     = [IsAuthenticated]
    serializer_class       = OrderSerializer

    def get(self, *args, **kwargs):
        date       = datetime.now()
        orders     = Order.objects.filter(timestamp__day=date.day, timestamp__month=date.month,
                                          timestamp__year=date.year, order_status="2")
        total_paid = sum(order.paid_amount for order in orders)
        total_due  = sum(order.due_amount for order in orders)
        total      = total_paid + total_due
        serializer = self.serializer_class(orders, many=True)
        return Response({"data": serializer.data, "total_paid": total_paid, "total_due": total_due,
                         "total": total}, status=status.HTTP_200_OK)



class TodayCashSaleItemsApiView(APIView):
    authentication_classes = [Authentication]
    permission_classes     = [IsAuthenticated]

    def get(self, *args, **kwargs):
        order_id   = kwargs["order_id"]
        order      = Order.objects.get(id=order_id, order_status="2")
        items      = order.orderItems.all()
        total_sales = sum(item.sub_total for item in items)
        total_qty = sum(item.quantity for item in items)
        total_profit = sum(item.profit for item in items)
        paid_amount  = order.paid_amount
        due_amount   = order.due_amount
        serializer = ResponseCartSerializer(items, many=True)
        return Response({"data": serializer.data, "total_sales": total_sales, "total_qty": total_qty,
                         "total_profit": total_profit, "paid_amount": paid_amount,
                         "due_amount": due_amount}, status=status.HTTP_200_OK)
