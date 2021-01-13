from django.contrib import admin
from django.contrib.auth.models import User
from django.urls import path, include, re_path

from rest_framework_jwt.views import obtain_jwt_token

from user import views
urlpatterns = [
    path('login/', obtain_jwt_token),
    path('register/', views.UsersView.as_view()),
    re_path(r'^(?P<username>\w{6,20})/count/$', views.UsernameIsExistedView.as_view()),
    re_path(r'^(?P<email>([\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+))/count/$', views.EmailIsExistedView.as_view())
]