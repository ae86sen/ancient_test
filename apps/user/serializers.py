import re

from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_jwt.utils import jwt_payload_handler, jwt_encode_handler


class UsersModelSerializer(serializers.ModelSerializer):
    # 父表获取字表信息
    # a.默认可以使用子表模型类名小写_set
    # interfaces_set = InterfacesModelSerializer(label='所拥有的接口', many=True)
    # b.如果某个字段返回的结果有多条，那么需要添加many=True参数
    # c.如果模型类中外键字段定义了related_name参数，那么会使用这个名称作为字段名
    # interfaces_set = serializers.StringRelatedField(many=True)
    # interfaces = serializers.StringRelatedField(many=True)
    password_confirm = serializers.CharField(min_length=6, max_length=20, write_only=True)
    token = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm', 'token')
        # exclude = ('desc', 'create_time', 'update_time')
        # read_only_fields = ('id', 'desc')
        # 可以在extra_kwargs属性中，来定制某些字段
        extra_kwargs = {
            'username': {
                'max_length': 20,
                'min_length': 6
            },
            'email': {
                'required': True,
                'write_only': True

            },
            'password': {
                'max_length': 20,
                'min_length': 6,
                'write_only': True,
            },
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError('密码和确认密码不一致')
        return attrs

    def validate_email(self, value):
        pattern = r'([\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+)'
        if re.match(pattern, value) is None:
            raise serializers.ValidationError('请输入正确的邮箱格式')
        return value

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        user.token = token
        return user