from django.db import models
from django.conf import settings



class Email(models.Model):
    SEND_STATUS = (
        ('Send', 'Send'),
        ('Draft', 'Draft')
    )
    sender     = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                   null=True, blank=True, related_name='sender')
    receiver   = models.EmailField(max_length=300)
    subject    = models.CharField(max_length=300, blank=True, null=True)
    email_body = models.TextField()
    read       = models.BooleanField(default=False)
    timestamp  = models.DateTimeField(auto_now_add=True)
    updated    = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pk)







