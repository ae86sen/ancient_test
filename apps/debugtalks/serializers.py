from rest_framework import serializers

from debugtalks.models import DebugTalks
from utils import common


class DebugTalksModelSerializer(serializers.ModelSerializer):
    project = serializers.StringRelatedField(help_text='项目名称')

    class Meta:
        model = DebugTalks
        fields = ('id', 'name', 'project','debugtalk')
        extra_kwargs = {
            'debugtalk': {
                'write_only': True
            }
        }
