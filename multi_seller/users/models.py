from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_seller = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)


class UserProfile(models.Model):  # Do not subclass AbstractUser here
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')  # Fixed related_name
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
