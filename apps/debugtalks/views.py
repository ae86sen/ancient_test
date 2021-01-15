from rest_framework import viewsets
from debugtalks.models import DebugTalks
from debugtalks.serializers import DebugTalksModelSerializer


class DebugTalksViewSet(viewsets.ModelViewSet):
    queryset = DebugTalks.objects.all()
    serializer_class = DebugTalksModelSerializer