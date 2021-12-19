from rest_framework import serializers
from .models import Email



class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Email
        fields = '__all__'



class SendEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Email
        fields = ['receiver', 'subject', 'email_body']



