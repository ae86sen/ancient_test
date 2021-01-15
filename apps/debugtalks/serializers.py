from rest_framework import serializers

from debugtalks.models import DebugTalks
from utils import common


class DebugTalksModelSerializer(serializers.ModelSerializer):
    project = serializers.StringRelatedField()

    class Meta:
        model = DebugTalks
        fields = ('id', 'name', 'project')
        # extra_kwargs = {
        #     'create_time': {
        #         'read_only': True,
        #         'format': common.datetime_fmt()
        #     }
        # }
