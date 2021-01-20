"""ancient_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path

from rest_framework.documentation import include_docs_urls

# from drf_yasg.views import get_schema_view
# from drf_yasg import openapi
# schema_view = get_schema_view(
#     openapi.Info(
#         title='古一的平台',  # 必填
#         default_version='v1',  # 必填
#         description='测试平台接口文档',
#         terms_of_service= '',
#         contact=openapi.Contact(email='1'),
#         license=openapi.License(name='BSD License')
#     ),
#     public=True,
# )

# urlpatterns = [
#    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=None), name='schema-json'),
#    path('swagger/', schema_view.with_ui('swagger', cache_timeout=None), name='schema-swagger-ui'),
#    path('redoc/', schema_view.with_ui('redoc', cache_timeout=None), name='schema-redoc'),
# ]
urlpatterns = [
    path('docs/', include_docs_urls(title='古一平台', description='测试平台接口文档')),
    path('api/', include('rest_framework.urls')),
    path('user/', include('user.urls')),
    path('', include('projects.urls')),
    path('', include('interfaces.urls')),
    path('', include('envs.urls')),
    path('', include('debugtalks.urls')),
    path('', include('testsuits.urls')),
    path('', include('reports.urls'))
]
