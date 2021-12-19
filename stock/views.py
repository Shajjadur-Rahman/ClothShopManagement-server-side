from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from account.authentication import Authentication
from rest_framework.permissions import IsAuthenticated
from expense.models import Expense
from .serializers import (
    CompanySerializer,
    ProductSerializer,
    CategorySerializer,
    AddProductSerializer,
    ImportInvoiceSerializer,
    CreateInvoiceSerializer,
    UpdateInvoiceSerializer,
    CreateCategorySerializer,
)
from rest_framework.generics import (
    ListAPIView,
    UpdateAPIView,
    CreateAPIView,
    DestroyAPIView,
    RetrieveAPIView,
)
from .models import (
    Company,
    Product,
    Category,
    ImportInvoice,
)

# =================================================================================
# Import invoice
# =================================================================================

class ImportInvoiceListApiView(ListAPIView):
    authentication_classes = [Authentication]
    permission_classes     = [IsAuthenticated]
    queryset               = ImportInvoice.objects.all()
    serializer_class       = ImportInvoiceSerializer


class AddInvoiceApiView(CreateAPIView):
    authentication_classes = [Authentication]
    permission_classes     = [IsAuthenticated]
    serializer_class       = CreateInvoiceSerializer
    queryset               = ImportInvoice.objects.all()


    def create(self, request, *args, **kwargs):
        try:
            invoice = ImportInvoice.objects.all().first()
            invoice_no = int(''.join(filter(lambda i: i.isdigit(), invoice.invoice_no)))
            invoice_no = str(invoice_no + 1)
        except Exception as e:
            invoice_no = str(1)
        invoice_no     = "invoice-" + invoice_no
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        saved_data  = serializer.save(invoice_no=invoice_no, imported_by=self.request.user, importer_name=self.request.user.username)
        expense_obj = Expense(expense_type=request.data.get("import_expense_type"),
                              expense_amount=request.data.get("import_expense"), entry_by=self.request.user,
                              creator_name=self.request.user.username, timestamp=request.data.get("timestamp"))
        expense_obj.invoice_id = saved_data.id
        expense_obj.save()
        serializer2 = ImportInvoiceSerializer(saved_data, many=False)
        return Response(serializer2.data, status=status.HTTP_200_OK)


class UpdateInvoiceApiView(APIView):
    authentication_classes = [Authentication]
    permission_classes     = [IsAuthenticated]
    serializer_class       = UpdateInvoiceSerializer

    def post(self, *args, **kwargs):
        try:
            invoice = ImportInvoice.objects.get(id=kwargs["id"])
        except Exception as e:
            return Response({"error": "Query does not exist !"})

        serializer    = self.serializer_class(instance=invoice, data=self.request.data)
        serializer.is_valid(raise_exception=True)
        saved_invoice = serializer.save()
        serializer2   = ImportInvoiceSerializer(saved_invoice, many=False)
        return Response(serializer2.data, status=status.HTTP_200_OK)







class DeleteInvoiceAiView(DestroyAPIView):
    authentication_classes = [Authentication]
    permission_classes     = [IsAuthenticated]
    queryset               = ImportInvoice.objects.all()
    serializer_class       = ImportInvoiceSerializer
    lookup_field           = "id"



# =================================================================================
# Company
# =================================================================================

class CompanyListApiView(ListAPIView):
    authentication_classes = [Authentication]
    permission_classes     = [IsAuthenticated]
    queryset               = Company.objects.all()
    serializer_class       = CompanySerializer




class CreateCompanyApiView(APIView):
    authentication_classes = [Authentication]
    permission_classes     = [IsAuthenticated]
    serializer_class         = CompanySerializer

    def post(self, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)



class UpdateCompanyApiView(APIView):
    authentication_classes = [Authentication]
    permission_classes     = [IsAuthenticated]
    serializer_class       = CompanySerializer

    def post(self, *args, **kwargs):
        try:
            company = Company.objects.get(id=kwargs["id"])
        except Exception as e:
            return Response({"error": "Query does not exist !"}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(instance=company, data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)



class DeleteCompanyApiView(DestroyAPIView):
    authentication_classes = [Authentication]
    permission_classes     = [IsAuthenticated]
    queryset               = Company.objects.all()
    serializer_class       = CompanySerializer
    lookup_field           = "id"






# =================================================================================
# Category
# =================================================================================

class CreateCategoryApiView(APIView):
    authentication_classes = [Authentication]
    permission_classes     = [IsAuthenticated]
    serializer_class       = CreateCategorySerializer

    def post(self, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        category = serializer.save()
        serializer2 = CategorySerializer(category, many=False)
        return Response(serializer2.data, status=status.HTTP_200_OK)



class CateGoryListApiView(ListAPIView):
    authentication_classes = [Authentication]
    permission_classes     = [IsAuthenticated]
    queryset               = Category.objects.all()
    serializer_class       = CategorySerializer



class UpdateCategoryApiView(APIView):
    authentication_classes = [Authentication]
    permission_classes     = [IsAuthenticated]
    serializer_class       = CreateCategorySerializer

    def post(self, *args, **kwargs):
        try:
            category = Category.objects.get(id=kwargs["id"])
        except Exception as e:
            return Response({"error": "Query does not exist !"})
        serializer = self.serializer_class(instance=category, data=self.request.data)
        serializer.is_valid(raise_exception=True)
        category = serializer.save()
        serializer2 = CategorySerializer(category, many=False)
        return Response(serializer2.data, status=status.HTTP_200_OK)


class DeleteCategoryApiView(DestroyAPIView):
    authentication_classes = [Authentication]
    permission_classes     = [IsAuthenticated]
    queryset               = Category.objects.all()
    lookup_field = "id"


# =================================================================================
# Product
# =================================================================================


class AddProductApiView(APIView):
    authentication_classes = [Authentication]
    permission_classes     = [IsAuthenticated]
    serializer_class       = AddProductSerializer

    def post(self, *args, **kwargs):
        try:
            product = Product.objects.all().first()
            product_id = int(''.join(filter(lambda i: i.isdigit(), product.product_id)))
            product_id = str(product_id + 1)
        except Exception as e:
            product_id = str(1)

        product_id = "P-" + product_id
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save(product_id=product_id)
        serializer2 = ProductSerializer(product, context={'request': self.request}, many=False)
        return Response(serializer2.data, status=status.HTTP_200_OK)



class ProductListApiView(ListAPIView):
    authentication_classes = [Authentication]
    permission_classes     = [IsAuthenticated]
    serializer_class       = ProductSerializer

    def get(self, *args, **kwargs):
        queryset   = Product.objects.filter(active=True)
        serializer = self.serializer_class(queryset, context={'request': self.request}, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductDetailApiView(RetrieveAPIView):
    authentication_classes = [Authentication]
    permission_classes     = [IsAuthenticated]
    queryset               = Product.objects.all()
    serializer_class       = ProductSerializer
    lookup_field           = "id"


class UpdateProductApiView(APIView):
    authentication_classes = [Authentication]
    permission_classes     = [IsAuthenticated]
    serializer_class       = AddProductSerializer

    def post(self, *args, **kwargs):
        try:
            product = Product.objects.get(id=kwargs["id"])
        except Exception as e:
            return Response({"error": "Query does not exists !"}, status=status.HTTP_404_NOT_FOUND)

        serializer  = self.serializer_class(instance=product, data=self.request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        serializer2 = ProductSerializer(product, context={'request': self.request}, many=False)
        return Response(serializer2.data, status=status.HTTP_200_OK)



class HideProductApiView(APIView):
    authentication_classes = [Authentication]
    permission_classes     = [IsAuthenticated]
    serializer_class       = ProductSerializer

    def post(self, *args, **kwargs):
        try:
            product = Product.objects.get(id=kwargs["id"])
        except Exception as e:
            return Response({"error": "Query does not exists !"}, status=status.HTTP_404_NOT_FOUND)

        serializer  = self.serializer_class(instance=product, data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"success": "Task updated !"}, status=status.HTTP_200_OK)



class DeactivateProductsApiView(APIView):
    authentication_classes = [Authentication]
    permission_classes     = [IsAuthenticated]
    serializer_class       = ProductSerializer

    def get(self, *args, **kwargs):
        queryset   = Product.objects.filter(active=False)
        serializer = self.serializer_class(queryset, context={'request': self.request}, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)





class InvoiceRelatedProductsApiView(APIView):
    authentication_classes = [Authentication]
    permission_classes     = [IsAuthenticated]

    def get(self, *args, **kwargs):
        try:
            invoice = ImportInvoice.objects.get(id=kwargs["invoice_id"])
        except Exception as e:
            return Response({"error": "Invoice query does not exist !"})
        products      = Product.objects.filter(invoice_id=kwargs["invoice_id"])
        total_import  = sum(item.price for item in products)
        total_item    = products.count()
        import_expense = invoice.import_expense
        serializer = ProductSerializer(products, context={'request': self.request}, many=True)
        return Response({"data": serializer.data, "total_import": total_import,
                         "total_item": total_item, "import_expense": import_expense}, status=status.HTTP_200_OK)

