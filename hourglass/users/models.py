from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    note = models.TextField(max_length=250, null=True, blank=True)
    phone = models.CharField(max_length=21, null=True, blank=True)
    location = models.CharField(max_length=32, null=True, blank=True)
