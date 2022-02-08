"""
Auth routines module
"""

from rest_framework import views
from rest_framework.response import Response
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import login


User = get_user_model()


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name',)


class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True)
    photo_url = serializers.SerializerMethodField(allow_null=True)

    class Meta:
        model = User
        fields = ('username', 'id', 'groups', 'first_name', 'last_name', 'email', 'photo_url', 'phone')

    def get_photo_url(self, instance):
        return instance.photo_url


class CurrentUserView(views.APIView):
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({'user': serializer.data})

    def post(self, request):
        serializer = UserSerializer(request.user)
        return Response({'user': serializer.data})





class ExtendedTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        login(self.context['request'], self.user)

        return data


class ExtendedTokenObtainPairView(TokenObtainPairView):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """
    serializer_class = ExtendedTokenObtainPairSerializer

    def get_serializer_context(self):
        context = super(ExtendedTokenObtainPairView, self).get_serializer_context()
        context.update({"request": self.request})
        return context