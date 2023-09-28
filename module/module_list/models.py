from django.db import models
from autoTest.base.base_model import BaseModel
from project.project_list.models import ProjectList


# Create your models here.
class ModuleList(BaseModel):
    """模块基本信息"""
    module_id = models.BigIntegerField(help_text="模块id", primary_key=True)
    module_name = models.SlugField(max_length=128, help_text="模块名", unique=True)
    module_version = models.CharField(max_length=128, default='V0.0.1', blank=True, help_text="模块版本号")
    module_desc = models.CharField(max_length=512, null=True, help_text="模块描述")
    is_disable = models.BooleanField(default=False, help_text='是否禁用')
    is_delete = models.BooleanField(default=False, help_text='逻辑删除')
    editor = models.CharField(max_length=128, default='admin', help_text="编辑者")
    belong_project = models.ForeignKey(to=ProjectList, on_delete=models.DO_NOTHING, db_constraint=False, related_name='module')

    class Meta:
        db_table = 'module'
        verbose_name = '模块基本信息'
        verbose_name_plural = verbose_name

    def delete(self, using=None, keep_parents=False):
        """重写数据库删除方法实现逻辑删除"""
        self.is_delete = True
        self.save()
