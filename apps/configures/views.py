import json

from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from configures.models import Configures
from configures.serializers import ConfiguresModelSerializer
from interfaces.models import Interfaces
from utils import handle_datas


class ConfiguresViewSet(viewsets.ModelViewSet):
    queryset = Configures.objects.all()
    serializer_class = ConfiguresModelSerializer

    def retrieve(self, request, *args, **kwargs):
        configure_obj = self.get_object()
        interface_id = configure_obj.interface_id
        project_id = Interfaces.objects.get(id=interface_id).project_id
        config_data = json.loads(configure_obj.request)
        request_data = config_data.get('config').get('request')

        # 处理配置中的请求头
        config_header = request_data.get('headers')
        header = handle_datas.handle_data4(config_header)

        # 处理配置中的变量
        config_variables = request_data.get('variables')
        variables = handle_datas.handle_data2(config_variables)

        datas = {
            'author': configure_obj.author,
            'configure_name': configure_obj.name,
            'selected_interface_id': interface_id,
            'selected_project_id': project_id,
            'header': header,
            'globalVar': variables  # 变量
        }
        return Response(datas)

