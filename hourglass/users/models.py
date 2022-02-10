from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver

from django_extensions.db.models import TimeStampedModel

class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()
    note = models.TextField(max_length=250, null=True, blank=True)
    phone = models.CharField(max_length=21, null=True, blank=True)
    location = models.CharField(max_length=32, null=True, blank=True)
    photo = models.FileField(null=True, blank=True)
    first_name = models.CharField('First name', max_length=30)
    last_name = models.CharField('Last name', max_length=150)
    email = models.EmailField('Mail to')
    username = models.CharField(
        "Email",
        max_length=150,
        unique=True,
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
        validators=[username_validator],
        error_messages={
            'unique': "A user with that username already exists.",
        },
    )

    @property
    def photo_url(self):
        if self.photo:
            return self.photo.url


class AuditUserEntry(TimeStampedModel):

    action = models.CharField(max_length=64)
    ip = models.GenericIPAddressField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __unicode__(self):
        return '{0} - {1} - {2}'.format(self.action, self.user.username, self.ip)


@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):

    ip = request.META.get('REMOTE_ADDR')
    AuditUserEntry.objects.create(action='user_logged_in', ip=ip, user=user)


@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):

    ip = request.META.get('REMOTE_ADDR')
    AuditUserEntry.objects.create(action='user_logged_out', ip=ip, username=user)
