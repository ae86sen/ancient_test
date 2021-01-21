from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from configures.models import Configures
from interfaces import serializers
from interfaces.models import Interfaces
from interfaces.serializers import InterfacesModelSerializer
from projects.models import Projects
from testcases.models import Testcases


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

    def get_serializer_class(self):
        """
        不同的action选择不同的序列化器
        :return:
        """
        if self.action == "testcases":
            return serializers.TestcasesByInterfaceIdModelSerializer
        elif self.action == "configs":
            return serializers.ConfiguresByInterfaceIdModelSerializer
        else:
            return self.serializer_class