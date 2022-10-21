from django.db import models
from autoTest.base.base_model import BaseModel


# Create your models here.
class ProjectList(BaseModel):
    """项目基本信息"""
    project_id = models.AutoField(help_text="项目id", primary_key=True)
    project_name = models.SlugField(max_length=128, help_text="项目名", unique=True)
    project_version = models.CharField(max_length=128, default='V0.0.1', blank=True, help_text="项目版本号")
    project_desc = models.CharField(max_length=512, null=True, help_text="项目描述")
    is_disable = models.BooleanField(default=False, help_text='是否禁用')
    is_delete = models.BooleanField(default=False, help_text='逻辑删除')
    editor = models.CharField(max_length=128, default='admin', help_text="编辑者")

    class Meta:
        db_table = 'project'
        verbose_name = '项目基本信息'
        verbose_name_plural = verbose_name

    def delete(self, using=None, keep_parents=False):
        """重写数据库删除方法实现逻辑删除"""
        self.is_delete = True
        self.save()
