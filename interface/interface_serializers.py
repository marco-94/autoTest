"""
接口管理的全部序列化器
"""
from rest_framework import serializers
from interface.models import ErpLogin, ApiInfo
from autoTest.base.base_serializers import BaseSerializer


class ErpLoginSerializer(BaseSerializer):
    """编辑模块信息"""
    username = serializers.CharField(required=True, help_text='用户手机号')
    password = serializers.CharField(required=True, help_text='用户密码')
    environment = serializers.IntegerField(required=True, help_text='测试环境：1：测试环境；2：正式环境')

    class Meta:
        model = ErpLogin

        fields = ('username', 'password', 'environment',)


class InterfaceQuickTestSerializer(BaseSerializer):
    """接口快速测试"""
    request_type = serializers.IntegerField(required=True, help_text="请求方式：1：get；2：post；3：put；4：delete")
    api_address = serializers.CharField(required=True, help_text="接口地址")
    request_parameter_type = serializers.IntegerField(required=True,
                                                      help_text="请求参数格式：1：表单(form-data)；2：源数据(raw)；3：Restful")
    headers = serializers.DictField(required=False, help_text="请求头信息")
    params = serializers.DictField(required=False, help_text="直传传参")
    data = serializers.DictField(required=False, help_text="json传参")

    class Meta:
        model = ApiInfo

        fields = (
            'request_type',
            'api_address',
            'request_parameter_type',
            'headers',
            'params',
            'data')
