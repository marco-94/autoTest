from django.db import models
from autoTest.base.base_model import *
from case.case_list.models import CaseList
from caseGroup.models import CaseGroupList
from module.module_list.models import ModuleList
from project.project_list.models import ProjectList
from autoTest.common.file_storage import FileStorage
from autoTest.common.global_configuration import global_id

HTTP_CHOICE = (
    ('HTTP', 'HTTP'),
    ('HTTPS', 'HTTPS')
)

REQUEST_TYPE_CHOICE = (
    ('POST', 'POST'),
    ('GET', 'GET'),
    ('PUT', 'PUT'),
    ('DELETE', 'DELETE')
)

REQUEST_PARAMETER_TYPE_CHOICE = (
    ('form-data', '表单(form-data)'),
    ('raw', '源数据(raw)'),
    ('Restful', 'Restful')
)


class ErpLogin(BaseModel):
    username = models.SlugField(max_length=128, help_text="用户名", unique=True)
    password = models.CharField(max_length=512, help_text="用户密码", unique=True)
    environment = models.IntegerField(max_length=128, help_text="测试环境", unique=True)
    token = models.CharField(max_length=512, help_text="token")

    # 指定数据库表信息
    class Meta:
        db_table = 'erp_login'
        verbose_name = 'erp用户登录'
        verbose_name_plural = verbose_name


class ApiInfo(BaseModel):
    api_id = models.BigIntegerField(help_text="接口id", primary_key=True)
    api_name = models.SlugField(max_length=128, help_text="接口名称", unique=True)
    http_type = models.CharField(max_length=50, default='HTTP', verbose_name='http/https', choices=HTTP_CHOICE)
    request_type = models.CharField(max_length=50, verbose_name='请求方式', choices=REQUEST_TYPE_CHOICE)
    api_address = models.CharField(max_length=1024, verbose_name='接口地址')
    request_parameter_type = models.CharField(max_length=50,
                                              verbose_name='请求参数格式',
                                              choices=REQUEST_PARAMETER_TYPE_CHOICE)
    headers = models.TextField(blank=True, null=True, verbose_name='请求头')
    data = models.TextField(blank=True, null=True, verbose_name='入参')
    api_version = models.CharField(max_length=128, default='V0.0.1', blank=True, help_text="接口版本号")
    api_desc = models.CharField(max_length=512, null=True, help_text="接口描述")
    is_disable = models.BooleanField(default=False, help_text='是否禁用')
    is_delete = models.BooleanField(default=False, help_text='逻辑删除')
    editor = models.CharField(max_length=128, default='admin', help_text="编辑者")

    class Meta:
        db_table = 'api_info'
        verbose_name = '接口基本信息'
        verbose_name_plural = verbose_name

    def delete(self, using=None, keep_parents=False):
        """重写数据库删除方法实现逻辑删除"""
        self.is_delete = True
        self.save()


class OssFile(BaseModel):
    file_id = models.BigIntegerField(help_text="文件id", primary_key=True)
    file_path = models.FileField(upload_to='uploads/', verbose_name='文件路径')
    file_name = models.CharField(max_length=512, blank=True, null=True, verbose_name='文件名')
    file_type = models.CharField(max_length=512, blank=True, null=True, verbose_name='文件类型')
    file_size = models.CharField(max_length=512, blank=True, null=True, verbose_name='文件大小')
    remark = models.TextField(blank=True, null=True, verbose_name='备注信息')
    editor = models.CharField(max_length=128, default='admin', help_text="编辑者")

    def __str__(self):
        return str(self.file_path)

    class Meta:
        db_table = 'oss_info'
        verbose_name_plural = "文件信息"
        verbose_name = verbose_name_plural
        unique_together = ('file_path',)


class OssFiles(BaseModel):
    file_id = models.AutoField(help_text="文件id", primary_key=True)
    file_path = models.FileField(upload_to='uploads/', verbose_name='文件路径', storage=FileStorage)
    file_name = models.CharField(max_length=512, blank=True, null=True, verbose_name='文件名')
    file_type = models.CharField(max_length=512, blank=True, null=True, verbose_name='文件类型')
    file_size = models.CharField(max_length=512, blank=True, null=True, verbose_name='文件大小')
    remark = models.TextField(blank=True, null=True, verbose_name='备注信息')
    editor = models.CharField(max_length=128, default='admin', help_text="编辑者")

    def __str__(self):
        return str(self.file_path)

    class Meta:
        db_table = 'oss_file'
        verbose_name_plural = "文件信息"
        verbose_name = verbose_name_plural
        unique_together = ('file_path',)
