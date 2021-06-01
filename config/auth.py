"""
Auth routines module
"""

from rest_framework import views
from rest_framework.response import Response
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group


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
