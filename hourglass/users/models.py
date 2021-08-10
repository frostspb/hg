from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    note = models.TextField(max_length=250, null=True, blank=True)
    phone = models.CharField(max_length=21, null=True, blank=True)
    location = models.CharField(max_length=32, null=True, blank=True)
    photo = models.FileField(null=True, blank=True)
    first_name = models.CharField('First name', max_length=30)
    last_name = models.CharField('Last name', max_length=150)
    email = models.EmailField('Email address')

    @property
    def photo_url(self):
        if self.photo:
            return self.photo.url
