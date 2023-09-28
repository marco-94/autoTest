from django.db import models
from autoTest.base.base_model import BaseModel
from caseGroup.models import CaseGroupList
from module.module_list.models import ModuleList
from project.project_list.models import ProjectList
from case.case_list.models import CaseList


# Create your models here.
class ReportList(BaseModel):
    """用例基本信息"""
    report_id = models.BigIntegerField(help_text="报告id", primary_key=True)
    report_name = models.SlugField(max_length=128, help_text="报告名", unique=True)
    report_desc = models.CharField(max_length=512, null=True, help_text="报告描述")
    editor = models.CharField(max_length=128, default='admin', help_text="编辑者")
    case = models.ForeignKey(to=CaseList,
                             default="",
                             on_delete=models.DO_NOTHING,
                             db_constraint=False,
                             null=False,
                             related_name='case_report',
                             help_text="所属用例")
    group = models.ForeignKey(to=CaseGroupList,
                              default="",
                              on_delete=models.DO_NOTHING,
                              db_constraint=False,
                              null=False,
                              related_name='report_group',
                              help_text="所属用例组")

    class Meta:
        db_table = 'report'
        verbose_name = '报告基本信息'
        verbose_name_plural = verbose_name
