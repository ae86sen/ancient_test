from rest_framework import serializers

from interfaces.models import Interfaces
from projects.models import Projects
# from projects.serializers import ProjectsModelSerializer
from utils import common


class InterfacesModelSerializer(serializers.ModelSerializer):
    project = serializers.StringRelatedField()
    project_id = serializers.PrimaryKeyRelatedField(queryset=Projects.objects.all(), write_only=True)

    class Meta:
        model = Interfaces
        exclude = ['update_time']
        extra_kwargs = {
            'create_time': {
                'read_only': True,
                'format': common.datetime_fmt()
            }
        }

    def create(self, validated_data):
        validated_data['project_id'] = validated_data['project_id'].id
        return super().create(validated_data)
        # pass
        # pass