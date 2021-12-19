from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import ugettext_lazy


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email must be set !")

        email = self.normalize_email(email)
        user  = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPE = (
        ('Admin', 'Admin'),
        ('Employee', 'Employee'),
        ('Client', 'Client'),
    )
    user_type  = models.CharField(max_length=10, choices=USER_TYPE, default='Admin')
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name  = models.CharField(max_length=50, blank=True, null=True)
    username   = models.CharField(max_length=50, blank=True, null=True)
    email      = models.EmailField(unique=True, null=False)
    is_staff   = models.BooleanField(
        ugettext_lazy("Staff Status"),
        default=False,
        help_text="Designates whether user can login this site !"
    )
    is_active = models.BooleanField(
        ugettext_lazy("Active"),
        default=True,
        help_text="Designates whether user treated as an active user ! Unselect this in stated of deleting "
                  "account !"
    )
    objects = UserManager()
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email


def upload_profile_image(instance, filename):
    return '/'.join(['profile_image', str(instance.user.username), filename])


class Profile(models.Model):
    GENDER = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Others", "Others"),
    )
    user              = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_no       = models.CharField(max_length=500, unique=True, null=True, blank=True)
    phone             = models.CharField(max_length=100)
    nid_no            = models.CharField(max_length=300, null=True, blank=True)
    facebook_link     = models.URLField(null=True, blank=True)
    profile_image     = models.FileField(upload_to=upload_profile_image, null=True, blank=True)
    profile_image_url = models.URLField(max_length=1000, null=True, blank=True)
    gender            = models.CharField(max_length=10, choices=GENDER, default="Male")
    salary            = models.FloatField(default=0.00)
    address           = models.TextField(max_length=800, null=True, blank=True)
    timestamp         = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}' profile"

    class Meta:
        ordering = ['-timestamp', ]



class Jwt(models.Model):
    user      = models.OneToOneField(User, on_delete=models.CASCADE, related_name='login_user', null=True, blank=True)
    access    = models.TextField()
    refresh   = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    updated   = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pk)
