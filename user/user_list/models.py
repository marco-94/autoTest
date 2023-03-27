from django.db import models
import hashlib
from django.contrib.auth.models import AbstractUser
from autoTest.base.base_model import BaseModel
from autoTest.common.global_configuration import global_id


class Account(AbstractUser, BaseModel):
    user_id = models.BigIntegerField(help_text="用户id", primary_key=True, default=global_id()["work_id"])
    username = models.SlugField(max_length=128, help_text="用户名", unique=True)
    password = models.CharField(max_length=128, help_text="用户密码")
    is_disable = models.BooleanField(default=False, help_text='是否禁用')
    is_delete = models.BooleanField(default=False, help_text='逻辑删除')

    # 指定数据库表信息
    class Meta:
        db_table = 'user'
        verbose_name = '用户基础信息'
        verbose_name_plural = verbose_name

    # 重写save方法，新增密码md5加密逻辑
    def save(self, *args, **kwargs):
        md5 = hashlib.md5()
        md5.update(self.password.encode())
        self.password = md5.hexdigest()
        super(Account, self).save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        """重写数据库删除方法实现逻辑删除"""
        self.is_delete = True
        self.save()


class UserRole(BaseModel):
    user_role_id = models.BigIntegerField(help_text="用户登录id", primary_key=True, default=global_id()["work_id"])
    user_token = models.CharField(max_length=256, help_text="token")
    user_info = models.ForeignKey(to=Account, on_delete=models.DO_NOTHING, db_constraint=False,
                                  related_name='user_base', unique=True)

    # 指定数据库表信息
    class Meta:
        db_table = 'user_role'
        verbose_name = '用户登录信息'
        verbose_name_plural = verbose_name

    # 插拔式连表查询
    @property
    def user_name(self):
        return self.user_info.username

    @property
    def user_id(self):
        return self.user_info.user_id
