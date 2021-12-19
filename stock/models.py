from django.db import models
from django.conf import settings



def upload_product_image(instance, filename):
    return '/'.join(['product_image', str(instance.name), filename])


class ImportInvoice(models.Model):
    invoice_no          = models.CharField(max_length=1000)
    imported_by         = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    importer_name       = models.CharField(max_length=200)
    import_expense      = models.FloatField(default=0.00)
    import_expense_type = models.CharField(max_length=300)
    timestamp           = models.DateTimeField()

    def __str__(self):
        return self.invoice_no

    class Meta:
        ordering = ["-pk", ]



class Company(models.Model):
    company_name   = models.CharField(max_length=200)
    brand_name     = models.CharField(max_length=200)
    contact_no     = models.CharField(max_length=200)
    address        = models.TextField(max_length=500, null=True, blank=True)
    authorised_man = models.CharField(max_length=200, null=True, blank=True)
    auth_man_phone = models.CharField(max_length=200, null=True, blank=True)


    def __str__(self):
        return self.company_name

class Category(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    title   = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Product(models.Model):
    PRODUCT_TYPE = (
        ("Ladies", "Ladies"),
        ("Gents", "Gents"),
        ("Kids", "Kids"),
        ("Others", "Others"),
    )
    SIZE = (
        ("XXS", "XXS"),
        ("XS", "XS"),
        ("S", "S"),
        ("M", "M"),
        ("L", "L"),
        ("XL", "XL"),
        ("XXL", "XXL"),
        ("XXXL", "XXXL"),
    )
    product_id     = models.CharField(max_length=1000)
    invoice        = models.ForeignKey(ImportInvoice, on_delete=models.PROTECT, related_name='invoice_products')
    company        = models.ForeignKey(Company, on_delete=models.PROTECT, related_name='products')
    category       = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='cat_products')
    name           = models.CharField(max_length=350)
    p_type         = models.CharField(max_length=20, choices=PRODUCT_TYPE, default="XXS")
    size           = models.CharField(max_length=10, choices=SIZE, null=True, blank=True)
    product_color  = models.CharField(max_length=200, null=True, blank=True)
    p_image        = models.FileField(upload_to=upload_product_image, null=True, blank=True)
    p_image_url    = models.URLField(max_length=1000, blank=True, null=True)
    gsm            = models.CharField(max_length=200, null=True, blank=True)
    panna          = models.CharField(max_length=350, null=True, blank=True)
    len_qty        = models.FloatField(default=0.00)
    quantity       = models.PositiveIntegerField(null=True, blank=True)
    unit_tag       = models.CharField(max_length=200)
    price          = models.FloatField(default=0.00)
    min_sale_price = models.FloatField(default=0.00)
    active         = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-pk", ]



