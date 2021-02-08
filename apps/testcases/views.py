import json
import os

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from envs.models import Envs
from interfaces.models import Interfaces
from projects.models import Projects
from testcases.models import Testcases
from testcases.serializers import TestcasesModelSerializer, TestcasesRunSerializer
from utils import handle_datas, common
from ancient_test import settings
from datetime import datetime


class TestSuitsViewSet(viewsets.ModelViewSet):
    queryset = Testcases.objects.all()
    serializer_class = TestcasesModelSerializer

    def retrieve(self, request, *args, **kwargs):
        testcase_obj = self.get_object()
        # 获取配置信息
        include = json.loads(testcase_obj.include)
        selected_configure_id = include.get('config')
        # 获取接口信息
        selected_interface_id = testcase_obj.interface_id
        # 获取项目信息
        selected_project_id = Interfaces.objects.get(id=selected_interface_id).project_id
        # 获取前置用例
        selected_testcase_id = include.get('testcases')
        # 将request请求体转为字典
        request_full_data = json.loads(testcase_obj.request)
        request_data = request_full_data.get('test').get('request')
        # 获取请求方法
        method = request_data.get('method')
        # 获取请求地址
        url = request_data.get('url')

        # 处理请求数据，请求数据有可能是1、查询参数，2、json数据，3、form表单数据
        # 1、处理用例中的查询参数（有可能没有）
        testcase_params = request_data.get('params')
        params = handle_datas.handle_data4(testcase_params)
        # 2、处理用例中的json数据（有可能没有）
        testcase_json = request_data.get('json')
        json_variable = json.dumps(testcase_json, ensure_ascii=False)
        # 3、处理用例中的form表单数据 （有可能没有）
        testcase_data = request_data.get('data')
        data_variable = handle_datas.handle_data6(testcase_data)

        # 处理用例中的请求头（有可能没有）
        testcase_headers = request_data.get('headers')
        headers = handle_datas.handle_data4(testcase_headers)

        # 处理用例中的extract（有可能没有）
        testcase_extract = request_full_data.get('test').get('extract')
        extract = handle_datas.handle_data3(testcase_extract)

        # 处理用例中的validate
        testcase_validate = request_full_data.get('test').get('validate')
        validate = handle_datas.handle_data1(testcase_validate)

        # 处理用例中的variables
        testcase_variables = request_full_data.get('test').get('variables')
        variables = handle_datas.handle_data2(testcase_variables)

        # 处理用例中的parameters
        testcase_parameters = request_full_data.get('test').get('parameters')
        parameters = handle_datas.handle_data3(testcase_parameters)

        # 处理用例中的setup_hooks
        testcase_setup_hooks = request_full_data.get('test').get('setup_hooks')
        setup_hooks = handle_datas.handle_data5(testcase_setup_hooks)

        # 处理用例中的teardown_hooks
        testcase_teardown_hooks = request_full_data.get('test').get('teardown_hooks')
        teardown_hooks = handle_datas.handle_data5(testcase_teardown_hooks)

        datas = {
            "author": testcase_obj.author,
            "testcase_name": testcase_obj.name,
            "selected_configure_id": selected_configure_id,
            "selected_interface_id": selected_interface_id,
            "selected_project_id": selected_project_id,
            "selected_testcase_id": selected_testcase_id,

            "method": method,
            "url": url,
            "param": params,  # 查询参数
            "header": headers,
            "variable": data_variable,  # form表单请求数据
            "jsonVariable": json_variable,  # json请求数据

            "extract": extract,
            "validate": validate,
            "globalVar": variables,  # 变量
            "parameterized": parameters,  # 参数化数据
            "setupHooks": setup_hooks,
            "teardownHooks": teardown_hooks,
        }
        return Response(datas)

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
        # 生成用例yaml文件
        common.generate_testcase_file(instance, env, testcase_dir_path)
        # 执行用例并生成报告
        return common.run_testcase(instance, testcase_dir_path)

    def get_serializer_class(self):
        return TestcasesRunSerializer if self.action == 'run' else self.serializer_class
