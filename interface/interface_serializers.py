"""
接口管理的全部序列化器
"""
from rest_framework import serializers
from interface.models import *
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


class OssFileSerializer(BaseSerializer):
    """文件上传"""
    file_id = serializers.IntegerField(required=False, help_text='文件ID(无需填写)')
    file = serializers.FileField(source="file_path", required=True, help_text="选择文件")
    remark = serializers.CharField(required=False, help_text='备注信息')
    editor = serializers.CharField(required=False, help_text='创建人/更新人(无需填写)')
    file_size = serializers.CharField(required=False, help_text='文件大小(无需填写)')
    file_type = serializers.CharField(required=False, help_text='文件类型(无需填写)')
    file_name = serializers.CharField(required=False, help_text='文件名(无需填写)')

    class Meta:
        model = OssFile

        fields = (
            'file',
            'remark',
            'editor',
            'file_id',
            'file_size',
            'file_type',
            'file_name',
            "created_tm",
            "updated_tm",
            "create_tm_format",
            "update_tm_format")


class OssFilesSerializer(BaseSerializer):
    """文件上传"""
    file_id = serializers.IntegerField(read_only=True, help_text='文件ID')
    file = serializers.FileField(source="file_path", required=True, help_text="文件地址")
    remark = serializers.CharField(required=False, help_text='备注信息')
    editor = serializers.CharField(read_only=True, help_text='创建人/更新人')
    file_size = serializers.CharField(read_only=True, help_text='文件大小')
    file_type = serializers.CharField(read_only=True, help_text='文件类型')
    file_name = serializers.CharField(read_only=True, help_text='文件名')

    class Meta:
        model = OssFiles

        fields = (
            'file',
            'file_id',
            'remark',
            'editor',
            'file_size',
            'file_type',
            'file_name',
            "created_tm",
            "updated_tm",
            "create_tm_format",
            "update_tm_format")


class OssFileUpdateSerializer(BaseSerializer):
    """上传文件更新"""

    class Meta:
        model = OssFiles
        fields = '_all_'
