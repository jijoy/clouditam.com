from rest_framework import generics, status, permissions
from django.contrib.auth.models import User
from api.serializers import UserCreateSerializer, UserLoginSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response



class UserCreateView(generics.CreateAPIView):
    model = User
    serializer_class = UserCreateSerializer
    permission_classes = [
        permissions.AllowAny # Or anon users can't register
    ]

class UserLoginView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserLoginSerializer
    permission_classes = [
        permissions.AllowAny # Or anon users can't register
    ]