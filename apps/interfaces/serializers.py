from rest_framework import serializers

from configures.models import Configures
from interfaces.models import Interfaces
from projects.models import Projects
# from projects.serializers import ProjectsModelSerializer
from testcases.models import Testcases
from utils import common, validates


class InterfacesModelSerializer(serializers.ModelSerializer):
    project = serializers.StringRelatedField(label='所属项目名称', help_text='所属项目名称')
    # 前端传入id后，得到的是一个模型类对象，所以在创建或更新的时候，需要先转化成id
    project_id = serializers.PrimaryKeyRelatedField(queryset=Projects.objects.all(),
                                                    label='项目id', help_text='项目id',
                                                    write_only=True)

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
        # 传入project模型类对象或者project.id都可以
        # project = validated_data.pop('project_id')
        # validated_data['project'] = project
        # return super().create(validated_data)
        project = validated_data.pop('project_id')
        validated_data['project_id'] = project.id
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'project_id' in validated_data:
            project = validated_data.pop('project_id')
            validated_data['project'] = project
        return super().update(instance, validated_data)


class TestcasesNamesModelSerializer(serializers.ModelSerializer):
    """获取Testcases模型类对象的id和name"""
    class Meta:
        model = Testcases
        fields = ('id', 'name')


class TestcasesByInterfaceIdModelSerializer(serializers.ModelSerializer):
    """通过Interfaces模型类对象获取Testcases模型类对象的字段"""
    testcases = TestcasesNamesModelSerializer(many=True, read_only=True)

    class Meta:
        model = Interfaces
        fields = ('testcases', )


class ConfiguresNamesModelSerializer(serializers.ModelSerializer):
    """获取Configures模型类对象的id和name"""

    class Meta:
        model = Configures
        fields = ('id', 'name')


class ConfiguresByInterfaceIdModelSerializer(serializers.ModelSerializer):
    """通过Interfaces模型类对象获取Configures模型类对象的字段"""
    configures = ConfiguresNamesModelSerializer(many=True, read_only=True)

    class Meta:
        model = Interfaces
        fields = ('configures', )


class InterfacesRunSerializer(serializers.ModelSerializer):
    env_id = serializers.IntegerField(label='环境变量ID', help_text='环境变量ID',
                                      write_only=True, validators=[validates.is_existed_env_id])

    class Meta:
        model = Interfaces
        fields = ['id', 'env_id']