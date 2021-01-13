from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework import mixins

from user.serializers import UsersModelSerializer


class UsersView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UsersModelSerializer