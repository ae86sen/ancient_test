import os
from datetime import datetime
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from configures.models import Configures
from envs.models import Envs
from interfaces import serializers
from interfaces.models import Interfaces
from interfaces.serializers import InterfacesModelSerializer
from projects.models import Projects
from testcases.models import Testcases
from utils import common
from ancient_test import settings


class InterfacesViewSet(viewsets.ModelViewSet):
    queryset = Interfaces.objects.all()
    serializer_class = InterfacesModelSerializer

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        results = response.data['results']
        data_list = []
        for item in results:
            interface_id = item.get('id')
            testcases_count = Testcases.objects.filter(interface_id=interface_id).count()
            configures_count = Configures.objects.filter(interface_id=interface_id).count()
            item['testcases'] = testcases_count
            item['configures'] = configures_count
            data_list.append(item)
        response.data['results'] = data_list
        return response

    @action(methods=['get'], detail=True)
    def testcases(self, request, *args, **kwargs):
        """
        Returns a list of all the testcases names by interface id
        """
        response = self.retrieve(request, *args, **kwargs)
        response.data = response.data['testcases']
        return response

    @action(methods=['get'], detail=True)
    def configs(self, request, *args, **kwargs):
        """
        Returns a list of all the testcases names by interface id
        """
        response = self.retrieve(request, *args, **kwargs)
        response.data = response.data['configures']
        return response

    @action(methods=['post'], detail=True)
    def run(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        env_id = serializer.validated_data['env_id']
        testcase_dir_path = os.path.join(settings.SUITES_DIR, datetime.strftime(datetime.now(), '%Y%m%d%H%M%S%f'))
        # 在suites目录下创建一个以时间戳命名的路径
        os.mkdir(testcase_dir_path)
        env = Envs.objects.filter(id=env_id).first()

        testcase_list = Testcases.objects.filter(interface=instance)

        if not testcase_list.exists():
            data = {
                'ret': False,
                'msg': '此接口下无用例，无法运行'
            }
            return Response(data, status=400)

        # 3、遍历可执行用例对象列表，为每个用例生成yaml文件
        for testcase_obj in testcase_list:
            # 生成用例yaml文件
            common.generate_testcase_file(testcase_obj, env, testcase_dir_path)

        # 4、执行用例并生成报告
        return common.run_testcase(instance, testcase_dir_path)

    def get_serializer_class(self):
        """
        不同的action选择不同的序列化器
        :return:
        """
        if self.action == "testcases":
            return serializers.TestcasesByInterfaceIdModelSerializer
        elif self.action == "configs":
            return serializers.ConfiguresByInterfaceIdModelSerializer
        elif self.action == "run":
            return serializers.InterfacesRunSerializer
        else:
            return self.serializer_class