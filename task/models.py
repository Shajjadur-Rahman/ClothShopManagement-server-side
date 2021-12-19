from django.db import models
from django.conf import settings


class Task(models.Model):
    user             = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    task_creator     = models.CharField(max_length=50)
    task_description = models.TextField(max_length=1000)
    completed        = models.BooleanField(default=False)
    timestamp        = models.DateTimeField()
    updated          = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.task_creator



