from django.contrib import admin
from django.contrib.auth.models import User
from django.urls import path, include, re_path

from rest_framework_jwt.views import obtain_jwt_token

from user.views import UsersView

urlpatterns = [
    path('login/', obtain_jwt_token),
    path('register/', UsersView.as_view())
]