import json
import os

from django.http import StreamingHttpResponse
from django.shortcuts import render

# Create your views here.
from django.utils.encoding import escape_uri_path
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from ancient_test import settings
from reports.models import Reports
from reports.serializers import ReportsModelSerializer
from reports.utils import get_file_content


class ReportsViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin,
                     GenericViewSet):
    queryset = Reports.objects.all()
    serializer_class = ReportsModelSerializer

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        results = response.data['results']
        data_list = []
        for item in results:
            # 将1转化为Pass，将0转化为Fail
            result = 'Pass' if item['result'] else 'Fail'
            item['result'] = result
            data_list.append(item)
        response.data['results'] = data_list
        return response

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        try:
            response.data['summary'] = json.loads(response.data['summary'])
        except Exception as e:
            raise e
        return response

    @action(detail=True)
    def download(self, request, *args, **kwargs):
        pass
        # 1、获取html源码
        instance = self.get_object()
        html = instance.html
        name = instance.name
        # 2、获取测试报告所属目录路径
        report_dir = settings.REPORT_DIR
        # 3、生成html文件，存放到reports目录下
        report_full_dir = os.path.join(report_dir,name) + '.html'
        if not os.path.exists(report_full_dir):
            with open(report_full_dir,'w',encoding='utf-8') as f:
                f.write(html)
        # 4、获取文件流，返回给前端
        # 创建一个生成器，获取文件流，每次获取的是文件字节数据
        response = StreamingHttpResponse(get_file_content(report_full_dir))
        html_file_name = escape_uri_path(name + '.html')
        # 5、添加响应头
        # 直接使用Response对象['响应头名称'] = '值'
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = f"attachement; filename*=UTF-8''{html_file_name}"
        return response
