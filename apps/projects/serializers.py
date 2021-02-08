from rest_framework import serializers
from interfaces.models import Interfaces
from projects.models import Projects
from utils import common, validates


class InterfacesNamesModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interfaces
        fields = ('id', 'name')


class ProjectsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        exclude = ('update_time',)

        extra_kwargs = {
            'create_time': {
                'read_only': True,
                'format': common.datetime_fmt(),
            },

        }


class ProjectsNamesModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = ('id', 'name')


class InterfacesByProjectIdModelSerializer(serializers.ModelSerializer):
    interfaces = InterfacesNamesModelSerializer(many=True, read_only=True)

    class Meta:
        model = Projects
        fields = ('interfaces',)


class InterfacesByProjectIdModelSerializer1(serializers.ModelSerializer):
    # interfaces = InterfacesNamesModelSerializer(many=True, read_only=True)

    class Meta:
        model = Interfaces
        fields = ('id', 'name')


class ProjectsRunSerializer(serializers.ModelSerializer):
    env_id = serializers.IntegerField(label='环境变量ID', help_text='环境变量ID',
                                      write_only=True, validators=[validates.is_existed_env_id])

    class Meta:
        model = Projects
        fields = ['id', 'env_id']