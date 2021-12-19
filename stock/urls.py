from django.urls import path
from . import views

urlpatterns = [

    path('import-invoice-list/', views.ImportInvoiceListApiView.as_view(), name='import-invoice-list'),
    path('add-invoice/', views.AddInvoiceApiView.as_view(), name='add-invoice'),
    path('update-invoice/<int:id>/', views.UpdateInvoiceApiView.as_view(), name='update-invoice'),
    path('delete-invoice/<int:id>/', views.DeleteInvoiceAiView.as_view(), name='delete-invoice'),

    path('company-list/', views.CompanyListApiView.as_view(), name='company-list'),
    path('create-company/', views.CreateCompanyApiView.as_view(), name='create-company'),
    path('update-company/<int:id>/', views.UpdateCompanyApiView.as_view(), name='update-company'),
    path('delete-company/<int:id>/', views.DeleteCompanyApiView.as_view(), name='delete-company'),


    path('create-category/', views.CreateCategoryApiView.as_view(), name='create-category'),
    path('category-list/', views.CateGoryListApiView.as_view(), name='category-list'),
    path('update-category/<int:id>/', views.UpdateCategoryApiView.as_view(), name='update-category'),
    path('delete-category/<int:id>/', views.DeleteCategoryApiView.as_view(), name='delete-category'),


    path('add-product/', views.AddProductApiView.as_view(), name='add-product'),
    path('product-list/', views.ProductListApiView.as_view(), name='product-list'),
    path('product-detail/<int:id>/', views.ProductDetailApiView.as_view(), name='product-detail'),
    path('update-product/<int:id>/', views.UpdateProductApiView.as_view(), name='update-product'),
    path('hide-product/<int:id>/', views.HideProductApiView.as_view(), name='hide-product'),
    path('deactivate-products/', views.DeactivateProductsApiView.as_view(), name='deactivate-products'),


    path('invoice-related-products/<int:invoice_id>/', views.InvoiceRelatedProductsApiView.as_view(),
         name='invoice-related-products'),
]
