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
from testsuits.models import Testsuits

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
    names:
        返回项目id和名称
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
        data_list = []
        # item为一条项目数据所在的字典
        # 需要获取当前项目所属的接口总数、用例总数、配置总数、套件总数
        for item in results:
            # 获取项目id
            project_id = item.get('id')
            # 获取每个项目接口总数
            interfaces_count = Interfaces.objects.filter(project_id=project_id).count()
            # 获取每个接口用例总数
            testcase_qs = Interfaces.objects.annotate(testcase=Count('testcases')).values('id', 'testcase').filter(project_id=project_id)
            testcases_count = 0
            for one_dict in testcase_qs:
                testcases_count += one_dict.get('testcase')
            # 获取每个接口配置总数
            configure_qs = Interfaces.objects.values('id').annotate(configure=Count('configures')).filter(project_id=project_id)
            configures_count = 0
            for one_dict in configure_qs:
                configures_count += one_dict.get('configure')
            # 获取每个项目测试套件总数
            testsuits_count = Testsuits.objects.filter(project_id=project_id).count()
            item['interfaces'] = interfaces_count
            item['testcases'] = testcases_count
            item['testsuits'] = testsuits_count
            item['configures'] = configures_count
            data_list.append(item)
        response.data['results'] = data_list
        return response

    @action(methods=['get'], detail=False)
    def names(self, request, *args, **kwargs):
        # 过滤
        qs = self.get_queryset()
        # 分页
        # page = self.paginate_queryset(qs)
        # logger.info(page)
        # if page is not None:
        #     serializer = self.get_serializer(instance=page, many=True)
        #     return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(instance=qs, many=True)
        return Response(serializer.data)
        # return self.list(request, *args, **kwargs)

    @action(methods=['get'], detail=True)
    def interfaces(self, request, *args, **kwargs):
        # instance = self.get_object()
        # serializer_obj = self.get_serializer(instance=instance)
        response = self.retrieve(request,*args,**kwargs)
        response.data = response.data['interfaces']
        # 进行过滤和分页操作
        return response

    def get_serializer_class(self):
        # 如果action名字为names，就调用ProjectsNamesModelSerializer序列化器
        if self.action == 'names':
            return ProjectsNamesModelSerializer
        elif self.action == 'interfaces':
            return InterfacesByProjectIdModelSerializer
        else:
            return self.serializer_class
