from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Extends Django's AbstractUser model, adding 'photo' and 'date_birth' fields.

    The image uploaded via 'photo' field is stored in 'users_photos/' directory.

    Attributes:
        photo (ImageField): A field for storing user's photo, which is not mandatory.
        date_birth (DateField): A field for storing the user's date of birth, which is not mandatory.
    """
    photo = models.ImageField(upload_to='users_photos/', blank=True, null=True)
    date_birth = models.DateField(blank=True, null=True)
