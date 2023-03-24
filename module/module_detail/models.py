from django.db import models
from autoTest.base.base_model import BaseModel
from module.module_list.models import ModuleList


# Create your models here.
class ModuleDetail(BaseModel):
    """模块详情信息"""
    module_img = models.ImageField('module', upload_to='./img', blank=True, null=True)
    module_url = models.URLField(max_length=256, blank=True, null=True)
    module_info = models\
        .ForeignKey(to=ModuleList, on_delete=models.DO_NOTHING, db_constraint=False, related_name='module')

    class Meta:
        db_table = 'module_detail'
        verbose_name = '模块详情信息'
        verbose_name_plural = verbose_name

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
