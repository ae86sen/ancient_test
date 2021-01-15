from interfaces import views
from django.urls import path
from rest_framework.routers import SimpleRouter, DefaultRouter
from rest_framework.documentation import include_docs_urls

# 1、创建路由对象
router = SimpleRouter()
router.register('interfaces', views.InterfacesViewSet)
urlpatterns = [
]
urlpatterns += router.urls
