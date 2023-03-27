from django.db import models
from autoTest.base.base_model import BaseModel
from module.module_list.models import ModuleList
from project.project_list.models import ProjectList
from autoTest.common.global_configuration import global_id


# Create your models here.
class CaseGroupList(BaseModel):
    """用例组基本信息"""
    case_group_id = models.BigIntegerField(help_text="用例组id", primary_key=True, default=global_id()["work_id"])
    case_group_name = models.SlugField(max_length=128, help_text="用例组名", unique=True)
    case_group_version = models.CharField(max_length=128, default='V0.0.1', blank=True, help_text="用例组版本号")
    case_group_desc = models.CharField(max_length=512, null=True, help_text="用例组描述")
    is_disable = models.BooleanField(default=False, help_text='是否禁用')
    is_delete = models.BooleanField(default=False, help_text='逻辑删除')
    editor = models.CharField(max_length=128, default='admin', help_text="编辑者")
    module = models.ForeignKey(to=ModuleList, on_delete=models.DO_NOTHING, db_constraint=False, related_name='case_group')
    project = models.ForeignKey(default="", to=ProjectList, on_delete=models.DO_NOTHING, db_constraint=False, related_name='project')

    class Meta:
        db_table = 'case_group'
        verbose_name = '用例组基本信息'
        verbose_name_plural = verbose_name

    def delete(self, using=None, keep_parents=False):
        """重写数据库删除方法实现逻辑删除"""
        self.is_delete = True
        self.save()
