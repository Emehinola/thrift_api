from django.db import models
from django.utils import timezone

from django.contrib.auth.models import AbstractBaseUser
from .manager import CustomManager


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    is_admin = models.BooleanField(default=False, editable=False)
    date_created = models.DateTimeField(default=timezone.now, editable=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomManager()

    class Meta:
        db_table = 'users'