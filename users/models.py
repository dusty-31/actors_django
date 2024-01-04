from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    photo = models.ImageField(upload_to='users_photo/', blank=True, null=True)
    date_birth = models.DateField(blank=True, null=True)