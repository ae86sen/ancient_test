from rest_framework import serializers

from configures.models import Configures
from envs.models import Envs
from interfaces.models import Interfaces
from utils import common, validates


class InterfacesProjectsSerializer(serializers.ModelSerializer):
    project = serializers.StringRelatedField(label='所属项目', help_text='所属项目')
    pid = serializers.IntegerField(label='所属项目id', help_text='所属项目id', write_only=True,
                                   validators=[validates.is_existed_project_id])
    iid = serializers.IntegerField(label='所属接口id', help_text='所属接口id', write_only=True,
                                   validators=[validates.is_existed_interface_id])

    class Meta:
        model = Interfaces
        fields = ['name', 'project', 'pid', 'iid']
        extra_kwargs = {
            'name': {
                'read_only': True,
            }
        }

    def validate(self, attrs):
        pid = attrs.get('pid')
        iid = attrs.get('iid')
        if not Interfaces.objects.filter(id=iid, project_id=pid).exists():
            raise serializers.ValidationError('所属项目id与接口id不匹配')
        return attrs


class ConfiguresModelSerializer(serializers.ModelSerializer):
    interface = InterfacesProjectsSerializer(label='所属项目和接口', help_text='所属项目和接口')

    class Meta:
        model = Configures
        fields = ['id', 'name', 'interface', 'author', 'request']
        extra_kwargs = {
            'request': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        interface = validated_data.pop('interface')
        validated_data['interface_id'] = interface['iid']
        return super().create(validated_data)

    def update(self, instance, validated_data):
        interface = validated_data.pop('interface')
        validated_data['interface_id'] = interface['iid']
        return super().update(instance, validated_data)
