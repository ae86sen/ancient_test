from rest_framework import serializers

from envs.models import Envs
from interfaces.models import Interfaces
from projects.models import Projects


def is_existed_project_id(value):
    """
    校验项目id是否存在
    :param value:
    :return:
    """
    if not Projects.objects.filter(id=value).exists():
        raise serializers.ValidationError('项目id不存在')


def is_existed_interface_id(value):
    """
    校验接口id是否存在
    :param value:
    :return:
    """
    if not Interfaces.objects.filter(id=value).exists():
        raise serializers.ValidationError('接口id不存在')


def is_existed_env_id(value):
    """
    校验环境配置id是否存在
    :param value:
    :return:
    """
    if not Envs.objects.filter(id=value).exists():
        raise serializers.ValidationError('环境配置id不存在')