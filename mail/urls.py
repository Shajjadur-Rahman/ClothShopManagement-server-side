from django.urls import path
from . import views


urlpatterns = [
    path('send-email/', views.SendEmailApiView.as_view(), name='send-email'),
    path('all-sent-mails/', views.AllSentMailsApiView.as_view(), name='all-sent-mails'),
]
