from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('stock/', include('stock.urls')),
    path('order/', include('order.urls')),
    path('expense/', include('expense.urls')),
    path('income/', include('income.urls')),
    path('task/', include('task.urls')),
    path('mail/', include('mail.urls'))
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

