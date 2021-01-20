from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from envs.models import Envs
from envs.serializers import EnvsModelSerializer, EnvsNamesSerializer


class EnvsViewSet(viewsets.ModelViewSet):
    queryset = Envs.objects.all()
    serializer_class = EnvsModelSerializer

    @action(detail=False)
    def names(self, request, *args, **kwargs):
        qs = self.get_queryset()
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    def get_serializer_class(self):
        # if self.action == 'names':
        #     return EnvsNamesSerializer
        # else:
        #     return self.permission_classes
        return EnvsNamesSerializer if self.action == 'names' else self.serializer_class