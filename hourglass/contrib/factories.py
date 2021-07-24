from django.contrib.auth import get_user_model
from factory import DjangoModelFactory
from factory import fuzzy


from hourglass.clients.models import Client


class UserFactory(DjangoModelFactory):
    is_active = True

    class Meta:
        model = get_user_model()
        django_get_or_create = ["username"]


class ClientFactory(DjangoModelFactory):
    name = fuzzy.FuzzyText()
    active = True

    class Meta:
        model = Client
