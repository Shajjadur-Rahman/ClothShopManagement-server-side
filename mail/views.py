from django.shortcuts import render
from datetime import datetime
from .models import Email
from django.utils import timezone
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.response import Response
from account.authentication import Authentication
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    EmailSerializer,
    SendEmailSerializer
)
from rest_framework.generics import ListAPIView



# class SendEmailApiView(APIView):
#     authentication_classes = [Authentication]
#     permission_classes     = [IsAuthenticated]
#
#     def post(self, *args, **kwargs):
#         serializer  = SendEmailSerializer(data=self.request.data)
#         images      = dict(self.request.data.lists())["mailImages"]  # This is very important . Get multiple images
#
#         serializer.is_valid(raise_exception=True)
#         saved_email = serializer.save(sender=self.request.user)
#         if images:
#             for image in images:
#                 file_obj = File()
#                 file_obj.image = image
#                 file_obj.mail  = saved_email
#                 file_obj.save()
#         serializer2 = EmailSerializer(saved_email, many=False)
#         return Response(serializer2.data, status=status.HTTP_201_CREATED)


class SendEmailApiView(APIView):
    authentication_classes = [Authentication]
    permission_classes     = [IsAuthenticated]

    def post(self, *args, **kwargs):
        serializer  = SendEmailSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        saved_email = serializer.save(sender=self.request.user)
        serializer2 = EmailSerializer(saved_email, many=False)
        return Response(serializer2.data, status=status.HTTP_201_CREATED)


# Fetching all sent emails

class AllSentMailsApiView(ListAPIView):
    authentication_classes = [Authentication]
    permission_classes     = [IsAuthenticated]
    serializer_class       = EmailSerializer
    queryset               = Email.objects.all()