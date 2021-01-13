import json
import logging
import random

from faker import Faker
from django.http import HttpResponse, JsonResponse, Http404
from django.views import View
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.decorators import action
from django.db.models import Count
from rest_framework import permissions
from rest_framework import authentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from interfaces.models import Interfaces
from projects.models import Projects
from django.db import connection
from interfaces.serializers import InterfacesModelSerializer
from projects.serializers import ProjectsModelSerializer, \
    ProjectsNamesModelSerializer, \
    InterfacesByProjectIdModelSerializer

# 定义日志器用于记录日志，logging.getLogger('全局配置settings.py中定义的日志器名')
logger = logging.getLogger('mytest')


class ProjectsViewSet(viewsets.ModelViewSet):
    """
    list:
        获取项目列表
    retrieve:
        获取项目详情
    create:
        添加项目
    destroy:
        删除项目
    """
    queryset = Projects.objects.all()
    serializer_class = ProjectsModelSerializer
    # filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ["id", "name"]
    # 需要过滤哪些就写哪些，名字必须与模型类中字段一致
    filterset_fields = ["name", "id"]
    # authentication_classes = []
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        results = response.data['results']
        # item为一条项目数据所在的字典
        # 需要获取当前项目所属的接口总数、用例总数、配置总数、套件总数
        for item in results:
            # 获取项目id
            project_id = item.get('id')
            # 获取每个项目接口总数
            interface_count = Interfaces.objects.filter(project_id=project_id).count()
            # 获取每个接口用例总数
            testcase_count = Interfaces.objects.annotate(testcase=Count('testcases')).values('id', 'testcase')
            # 获取每个接口配置总数
            configure_count = Interfaces.objects.annotate(configure=Count('configures')).values('id', 'configure')
            # 获取每个项目测试套件总数
            testsuit_count = Projects.objects.annotate(testsuit=Count('testsuits')).values('id', 'testsuit').filter(id=project_id)
            pass

    @action(methods=['get'], detail=False, url_path='xxxx')
    def names(self, request, *args, **kwargs):
        # 过滤
        qs = self.filter_queryset(self.get_queryset())
        # 分页
        page = self.paginate_queryset(qs)
        logger.info(page)
        if page is not None:
            serializer = self.get_serializer(instance=page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(instance=qs, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=True)
    def interfaces(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer_obj = self.get_serializer(instance=instance)
        # 进行过滤和分页操作
        return Response(serializer_obj.data)

    def get_serializer_class(self):
        # 如果action名字为names，就调用ProjectsNamesModelSerializer序列化器
        if self.action == 'names':
            return ProjectsNamesModelSerializer
        elif self.action == 'interfaces':
            return InterfacesByProjectIdModelSerializer
        else:
            return self.serializer_class
