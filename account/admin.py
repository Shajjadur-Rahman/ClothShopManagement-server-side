from django.contrib import admin
from .models import User, Profile, Jwt

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Jwt)
