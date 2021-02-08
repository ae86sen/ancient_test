import re

from rest_framework import serializers

from interfaces.models import Interfaces
from projects.models import Projects
from testcases.models import Testcases
from testsuits.models import Testsuits
from utils import validates


class InterfacesProjectsModelSerializer(serializers.ModelSerializer):
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


class TestcasesModelSerializer(serializers.ModelSerializer):
    interface = InterfacesProjectsModelSerializer(label='所属项目和接口', help_text='所属项目和接口')

    class Meta:
        model = Testcases
        exclude = ['create_time', 'update_time']
        extra_kwargs = {
            'include': {
                'write_only': True,
                # 'validators': [validate_include]
            },
            'request': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        iid = validated_data.pop('interface').get('iid')
        validated_data['interface_id'] = iid
        return super().create(validated_data)

    def update(self, instance, validated_data):
        iid = validated_data.pop('interface').get('iid')
        validated_data['interface_id'] = iid
        return super().update(instance, validated_data)


class TestcasesRunSerializer(serializers.ModelSerializer):
    env_id = serializers.IntegerField(label='环境变量ID', help_text='环境变量ID',
                                      write_only=True, validators=[validates.is_existed_env_id])

    class Meta:
        model = Testcases
        fields = ['id', 'env_id']
