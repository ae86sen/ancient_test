import re

from rest_framework import serializers

from interfaces.models import Interfaces
from projects.models import Projects
from testsuits.models import Testsuits
from utils import common


def validate_include(value):
    obj = re.match(r'^\[\d+(,\d+)*\]$', value)
    if obj is None:
        raise serializers.ValidationError('输入参数格式有误')
    else:
        res = obj.group()
        try:
            data = eval(res)
        except:
            raise serializers.ValidationError('输入参数格式有误')
        for item in data:
            if not Interfaces.objects.filter(id=item).exists():
                raise serializers.ValidationError(f'接口id【{item}】不存在')


class TestsuitsModelSerializer(serializers.ModelSerializer):
    project = serializers.StringRelatedField()
    project_id = serializers.PrimaryKeyRelatedField(queryset=Projects.objects.all())

    class Meta:
        model = Testsuits
        fields = '__all__'
        extra_kwargs = {
            'create_time': {
                'format': common.datetime_fmt()
            },
            'update_time': {
                'format': common.datetime_fmt()
            },
            'include': {
                'write_only': True,
                'validators': [validate_include]
            }
        }

    def create(self, validated_data):
        project = validated_data.pop('project_id')
        validated_data['project_id'] = project.id
        return super().create(validated_data)

    def update(self, instance, validated_data):
        project = validated_data.pop('project_id')
        validated_data['project_id'] = project.id
        return super().update(instance,validated_data)
