from django.db import models
from user.user_list.models import BaseModel, Account


class UserDetail(BaseModel):
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
#
#
# # Create your models here.
# class UserDetail(models.Model):
#     id = models.AutoField(help_text="id", primary_key=True)
#     user_email = models.EmailField(blank=True, default="", help_text='用户邮箱')
#     user_introduction = models.CharField(max_length=128, help_text="用户简介")
#     nickname = models.CharField(max_length=128, help_text="用户昵称")
#     updated_tm = models.DateTimeField(auto_now=True)
#     created_tm = models.DateTimeField(auto_now_add=True)
#     user_info = models.ForeignKey(to=User, on_delete=models.DO_NOTHING, help_text='用户id', unique=True)
#
#     def __str__(self):
#         return self.nickname, self.user_email
#
#     @property
#     def u_info(self):
#         u_l = []
#         u = self.user_info.all()
#
#     # 指定数据库表信息
#     class Meta:
#         db_table = 'user_detail'
#         verbose_name = '用户详情信息'
#         verbose_name_plural = verbose_name
#


