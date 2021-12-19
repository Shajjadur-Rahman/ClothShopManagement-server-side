from rest_framework import serializers
from .models import (
    ImportInvoice,
    Company,
    Category,
    Product
)

class ImportInvoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model  = ImportInvoice
        fields = ["id", "invoice_no", "import_expense_type", "importer_name", "import_expense", "timestamp"]



class CreateInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model  = ImportInvoice
        fields = ["import_expense_type", "import_expense", "timestamp"]


class UpdateInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model  = ImportInvoice
        fields = ["id", "invoice_no", "import_expense_type", "import_expense", "timestamp"]



class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model  = Company
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model  = Category
        fields = "__all__"
        depth  = 2


class CreateCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class AddProductSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Product
        fields = ["invoice", "company", "category", "name", "p_type", "size", "product_color", "p_image", "p_image_url", "gsm",
                  "panna", "len_qty", "quantity", "unit_tag", "price", "min_sale_price"]




class ProductSerializer(serializers.ModelSerializer):
    p_image  = serializers.SerializerMethodField("get_p_image_url")

    class Meta:
        model  = Product
        fields = ["id", "product_id", "invoice", "company", "category", "name", "p_type", "size",
                  "product_color", "p_image", "p_image_url", "gsm", "panna", "len_qty", "quantity", "unit_tag", "price",
                  "min_sale_price", "active"]
        depth = 3

    def get_p_image_url(self, obj):
        request = self.context.get('request')
        if obj.p_image:
            product_image = obj.p_image.url
            return request.build_absolute_uri(product_image)
        return None






