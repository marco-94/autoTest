from django.db import models
from user.user_list.models import Account
from autoTest.base.base_model import BaseModel
from autoTest.common.global_configuration import global_id


class UserDetail(BaseModel):
    user_detail_id = models.BigIntegerField(help_text="用户详情id", primary_key=True, default=global_id()["work_id"])
    user_email = models.EmailField(blank=True, default="", help_text='用户邮箱')
    user_introduction = models.CharField(max_length=128, help_text="用户简介")
    nickname = models.CharField(max_length=128, help_text="用户昵称")
    user_info = models.ForeignKey(to=Account, on_delete=models.DO_NOTHING, db_constraint=False, related_name='user')

    # 指定数据库表信息
    class Meta:
        db_table = 'user_detail'
        verbose_name = '用户详情信息'
        verbose_name_plural = verbose_name

    # 插拔式连表查询
    @property
    def user_name(self):
        return self.user_info.username

    @property
    def user_id(self):
        return self.user_info.user_id



