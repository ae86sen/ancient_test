from rest_framework import serializers

from interfaces.models import Interfaces
from projects.models import Projects
# from projects.serializers import ProjectsModelSerializer


class InterfacesModelSerializer(serializers.ModelSerializer):
    # a.会将父表的主键id值作为返回值
    # projects = serializers.PrimaryKeyRelatedField(help_text='所属项目', label='所属项目', queryset=Projects.objects.all())
    # b.会将父表对应对象的__str__方法的结果返回
    # projects = serializers.StringRelatedField()
    # c.会将父表对应对象的某个字段的值返回
    # projects = serializers.SlugRelatedField(slug_field='leader', read_only=True)
    # d.可以将某个序列化器对象定义为字段，支持Field中的所有参数
    # projects = ProjectsModelSerializer(label='所属项目信息', help_text='所属项目信息', read_only=True)
    class Meta:
        model = Interfaces
        # fields = ('id', 'name', 'leader', 'tester', 'programmer', 'create_time', 'update_time', 'email')
        fields = '__all__'
