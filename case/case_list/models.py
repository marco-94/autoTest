from django.db import models
from autoTest.base.base_model import BaseModel
from caseGroup.models import CaseGroupList
from module.module_list.models import ModuleList
from project.project_list.models import ProjectList
from autoTest.common.global_configuration import global_id


# Create your models here.
class CaseList(BaseModel):
    """用例基本信息"""
    case_id = models.BigIntegerField(help_text="用例id", primary_key=True, default=global_id()["work_id"])
    case_name = models.SlugField(max_length=128, help_text="用例名", unique=True)
    case_version = models.CharField(max_length=128, default='V0.0.1', blank=True, help_text="用例版本号")
    case_desc = models.CharField(max_length=512, null=True, help_text="用例描述")
    is_disable = models.BooleanField(default=False, help_text='是否禁用')
    is_delete = models.BooleanField(default=False, help_text='逻辑删除')
    editor = models.CharField(max_length=128, default='admin', help_text="编辑者")
    group = models.ForeignKey(to=CaseGroupList,
                              on_delete=models.DO_NOTHING,
                              db_constraint=False,
                              related_name='case_group',
                              help_text="所属用例组")
    module = models.ForeignKey(to=ModuleList,
                               on_delete=models.DO_NOTHING,
                               db_constraint=False,
                               related_name='case_module',
                               help_text="所属模块")
    project = models.ForeignKey(default="",
                                to=ProjectList,
                                on_delete=models.DO_NOTHING,
                                db_constraint=False,
                                related_name='case_project',
                                help_text="所属项目")

    class Meta:
        db_table = 'case'
        verbose_name = '用例基本信息'
        verbose_name_plural = verbose_name

    def delete(self, using=None, keep_parents=False):
        """重写数据库删除方法实现逻辑删除"""
        self.is_delete = True
        self.save()
