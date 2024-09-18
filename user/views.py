from django.shortcuts import render
from rest_framework import generics
from tutorial.quickstart.serializers import UserSerializer

from user.models import User
from user.serializers import UserSerializer


# Create your views here.


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
