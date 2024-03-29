from django.db import models
from autoTest.base.base_model import BaseModel
from module.module_list.models import ModuleList
from autoTest.common.global_configuration import global_id


# Create your models here.
class ModuleDetail(BaseModel):
    """模块详情信息"""
    module_detail_id = models.BigIntegerField(help_text="模块详情id", primary_key=True)
    module_img = models.CharField(max_length=256, blank=True, null=True)
    module_url = models.CharField(max_length=256, blank=True, null=True)
    module_info = models\
        .ForeignKey(to=ModuleList, on_delete=models.DO_NOTHING, db_constraint=False, related_name='module')

    class Meta:
        db_table = 'module_detail'
        verbose_name = '模块详情信息'
        verbose_name_plural = verbose_name

    def save(self, *args, **kwargs):
        """新增时，自定义主键"""
        if not self.module_detail_id:
            self.module_detail_id = global_id()["work_id"]
        return super(ModuleDetail, self).save(*args, **kwargs)

    # 插拔式连表查询
    @property
    def module_id(self):
        return self.module_info.module_id

    @property
    def module_name(self):
        return self.module_info.module_name

    @property
    def module_desc(self):
        return self.module_info.module_desc

    @property
    def editor(self):
        return self.module_info.editor
