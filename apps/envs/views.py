from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from envs.models import Envs
from envs.serializers import EnvsModelSerializer


class EnvsViewSet(viewsets.ModelViewSet):
    queryset = Envs.objects.all()
    serializer_class = EnvsModelSerializer

    # def list(self, request, *args, **kwargs):
    #     response = super().list(request, *args, **kwargs)
    #     results = response.data['results']
    #     data_list = []
    #     for item in results:
    #         interface_id = item.get('id')
    #         project_name = item.get('project')
    #         project_id = Projects.objects.get(name=project_name).id
    #         testcases_count = Testcases.objects.filter(interface_id=interface_id).count()
    #         configures_count = Configures.objects.filter(interface_id=interface_id).count()
    #         # item['project'] = project_name
    #         item['project_id'] = project_id
    #         item['testcases'] = testcases_count
    #         item['configures'] = configures_count
    #         data_list.append(item)
    #     response.data['results'] = data_list
    #     return response

    # def create(self, request, *args, **kwargs):
    #     response = super().create(request, *args, **kwargs)
    #     project_id = response.data['project']
    #     project = Projects.objects.get(id=project_id).name
    #     response.data['project'] = project
    #     response.data['project_id'] = project_id
    #     return response