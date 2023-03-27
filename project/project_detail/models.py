from django.db import models
from autoTest.base.base_model import BaseModel
from project.project_list.models import ProjectList
from autoTest.common.global_configuration import global_id


# Create your models here.
class ProjectDetail(BaseModel):
    """项目详情信息"""
    project_detail_id = models.BigIntegerField(help_text="用户详情id", primary_key=True, default=global_id()["work_id"])
    project_img = models.ImageField('project', upload_to='./img', blank=True, null=True)
    project_url = models.URLField(max_length=256, blank=True, null=True)
    project_info = models\
        .ForeignKey(to=ProjectList, on_delete=models.DO_NOTHING, db_constraint=False, related_name='List')

    class Meta:
        db_table = 'project_detail'
        verbose_name = '项目详情信息'
        verbose_name_plural = verbose_name

    # 插拔式连表查询
    @property
    def project_id(self):
        return self.project_info.project_id

    @property
    def project_name(self):
        return self.project_info.project_name

    @property
    def project_desc(self):
        return self.project_info.project_desc

    @property
    def editor(self):
        return self.project_info.editor
