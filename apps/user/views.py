from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.views import APIView

from user.serializers import UsersModelSerializer


class UsersView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UsersModelSerializer


class UsernameIsExistedView(APIView):

    def get(self, request, username):
        count = User.objects.filter(username=username).count()
        one_dict = {
            'username': username,
            'count': count
        }
        return Response(one_dict)


class EmailIsExistedView(APIView):

    def get(self, request, email):
        count = User.objects.filter(email=email).count()
        one_dict = {
            'email': email,
            'count': count
        }
        return Response(one_dict)
