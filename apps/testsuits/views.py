from django.shortcuts import render

# Create your views here.
import os
from datetime import datetime

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from envs.models import Envs
from testcases.models import Testcases
from testsuits.models import Testsuits
from testsuits.serializers import TestsuitsModelSerializer,TestsuitsRunSerializer
from ancient_test import settings
from utils import common
from .utils import get_testcases_by_interface_ids


class TestSuitsViewSet(viewsets.ModelViewSet):
    queryset = Testsuits.objects.all()
    serializer_class = TestsuitsModelSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        data = {
            'name': instance.name,
            'project_id': instance.project_id,
            'include': instance.include
        }
        return Response(data)

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

        include = eval(instance.include)
        if len(include) == 0:
            data = {
                'ret': False,
                'msg': '此套件下未添加接口, 无法运行'
            }
            return Response(data, status=400)
        testcase_list = get_testcases_by_interface_ids(include)
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
        if self.action == "run":
            return TestsuitsRunSerializer
        else:
            return self.serializer_class