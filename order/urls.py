from django.urls import path
from . import views


urlpatterns = [
    path('search-customer/', views.SearchCustomerApiView.as_view(), name='search-customer'),
    path('add-to-cart/', views.AddToCartApiView.as_view(), name='add-to-cart'),
    path('remove-product/<int:product_id>/<int:customer_id>/<str:p_qty>/<str:type>/',
         views.RemoveProductApiView.as_view(),
         name='remove-product'),
    path('cart-view/<int:id>/', views.CartApiView.as_view(), name='cart-view'),
    path('complete-order/<str:paid_amount>/<int:id>/', views.CompleteOrderApiView.as_view(), name='complete-order'),
    path('order-in-year/', views.OrderInYearApiView.as_view(), name='order-in-year'),
    path('sale-in-month/<str:month>/<str:year>/', views.SaleInMonthApiView.as_view(), name='sale-in-month'),
    path('today-sale/', views.TodaySaleApiView.as_view(), name='today-sale'),
    path('today-due-sales/', views.TodayDueSalesApiView.as_view(), name='today-due-sales'),
    path('today-cash-sales/', views.TodayCashSalesApiView.as_view(), name='today-cash-sales'),
    path('today-due-sale-items/<int:order_id>/', views.TodayDueSaleItemsApiView.as_view(),
         name='today-due-sale-items'),
    path('today-cash-sale-items/<int:order_id>/', views.TodayCashSaleItemsApiView.as_view(),
         name='today-cash-sale-items'),
    path('clients/', views.ClientsApiView.as_view(), name='clients'),
    path('all-order/<int:customer_id>/', views.AllOrderApiView.as_view(), name="all-order"),
    path('due-order/<int:customer_id>/', views.DueOrderApiView.as_view(), name="due-order"),
    path('pay-due-amount/<str:paid_amount>/<int:order_id>/', views.PayDueAmountApiView.as_view(),
         name='pay-due-amount'),

    path('total-order-summary/', views.TotalOrderSummaryApiView.as_view(), name='total-order-summary'),
    path('sales-summary/', views.SaleAnalyticApiView.as_view(), name='sales-summary'),
    path('due-sales-summary/', views.DueSaleAnalyticApiView.as_view(), name='due-sales-summary'),
]
