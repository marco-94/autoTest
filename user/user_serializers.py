"""
用户管理的全部序列化器
"""
from rest_framework import serializers
from user.user_list.models import Account, UserRole, BaseModel
from user.user_detail.models import UserDetail
import time


class BaseSerializer(serializers.ModelSerializer):
    """基类序列化器"""
    create_tm_format = serializers.DateTimeField(source="created_tm",
                                                 format="%Y-%m-%d %H:%M:%S",
                                                 required=False,
                                                 read_only=True,
                                                 help_text='创建时间')
    update_tm_format = serializers.DateTimeField(source="updated_tm",
                                                 format="%Y-%m-%d %H:%M:%S",
                                                 required=False,
                                                 read_only=True,
                                                 help_text='更新时间')

    # 重写方法，返回时间戳
    def to_representation(self, instance):
        data = super().to_representation(instance)
        create_time = data.get("create_tm_format")
        update_time = data.get("update_tm_format")
        if create_time and update_time:
            create_time_stamp = str((time.mktime(time.strptime(create_time, '%Y-%m-%d %H:%M:%S'))) * 1000).split(".")[0]
            update_time_stamp = str((time.mktime(time.strptime(update_time, '%Y-%m-%d %H:%M:%S'))) * 1000).split(".")[0]
            data.update({"created_tm": create_time_stamp, "updated_tm": update_time_stamp})
            return data

    class Meta:
        model = BaseModel
        fields = ("created_tm", "updated_tm", "create_tm_format", "update_tm_format")


class LoginSerializer(serializers.ModelSerializer):
    """登录入参序列化器"""
    user_id = serializers.IntegerField(read_only=True)
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Account

        fields = ('username', 'password', 'user_id')


class PasswordSerializer(serializers.ModelSerializer):
    """修改密码入参序列化器"""
    user_id = serializers.IntegerField(write_only=True, help_text='用户ID')
    old_password = serializers.CharField(write_only=True, help_text='旧密码')
    new_password = serializers.CharField(write_only=True, help_text='新密码')
    confirm_password = serializers.CharField(write_only=True, help_text='确认新密码')

    class Meta:
        model = Account

        fields = ('user_id', 'old_password', 'new_password', 'confirm_password')


class UserSerializer(BaseSerializer):
    """用户基本信息"""

    # 设置只读只写
    is_disable = serializers.BooleanField(read_only=True)
    username = serializers.CharField(required=False)

    # 设置非必填
    user_introduction = serializers.CharField(required=False)
    nickname = serializers.CharField(required=False)
    created_start_tm = serializers.IntegerField(write_only=True, required=False)
    created_end_tm = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Account

        fields = ('user_id',
                  'username',
                  'email',
                  'created_start_tm',
                  'created_end_tm',
                  'is_disable',
                  'user_introduction',
                  'nickname', "created_tm", "updated_tm", "create_tm_format", "update_tm_format"
                  )

        # exclude = ['date_joined']


class UserRoleSerializer(BaseSerializer):
    """用户登录信息"""

    class Meta:
        model = UserRole

        # 定义需要返回的字段及顺序
        fields = ('id',
                  'user_id',
                  'user_name',
                  'user_token',
                  'create_tm_format',
                  'update_tm_format')


class UserDetailSerializer(BaseSerializer):
    """用户详情信息"""

    class Meta:
        model = UserDetail

        fields = ('id',
                  'user_id',
                  'user_name',
                  'nickname',
                  'user_email',
                  'user_introduction',
                  'create_tm_format',
                  'update_tm_format')
