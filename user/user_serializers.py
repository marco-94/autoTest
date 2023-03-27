"""
用户管理的全部序列化器
"""
from rest_framework import serializers
from user.user_list.models import Account, UserRole
from user.user_detail.models import UserDetail
from autoTest.base.base_serializers import BaseSerializer


class LoginSerializer(serializers.ModelSerializer):
    """登录入参序列化器"""
    user_id = serializers.IntegerField(read_only=True, help_text="用户ID")
    username = serializers.CharField(write_only=True, required=True, help_text="用户名", min_length=5, max_length=20)
    password = serializers.CharField(write_only=True, required=True, help_text="密码", min_length=8, max_length=20)

    class Meta:
        model = Account

        fields = ('username', 'password', 'user_id')


class PasswordSerializer(serializers.ModelSerializer):
    """修改密码入参序列化器"""
    user_id = serializers.IntegerField(write_only=True, help_text='用户ID')
    old_password = serializers.CharField(write_only=True, help_text='旧密码', min_length=8, max_length=20)
    new_password = serializers.CharField(write_only=True, help_text='新密码', min_length=8, max_length=20)
    confirm_password = serializers.CharField(write_only=True, help_text='确认新密码', min_length=8, max_length=20)

    class Meta:
        model = Account

        fields = ('user_id', 'old_password', 'new_password', 'confirm_password')


class UserListSerializer(BaseSerializer):
    """用户基本信息"""
    user_id = serializers.CharField(required=False, help_text="用户ID")
    is_disable = serializers.BooleanField(required=False, help_text="用户状态")
    username = serializers.CharField(required=False, help_text="用户名")
    user_introduction = serializers.CharField(read_only=True, help_text="用户介绍")
    nickname = serializers.CharField(read_only=True, help_text="昵称")
    created_start_tm = serializers.IntegerField(read_only=True)
    created_end_tm = serializers.IntegerField(read_only=True)

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


class UserCreateSerializer(BaseSerializer):
    """用户新增"""

    username = serializers.CharField(required=True, min_length=5, max_length=20, help_text="用户名")
    password = serializers.CharField(required=True, min_length=8, max_length=20, help_text="密码")
    email = serializers.CharField(required=False, help_text="邮箱")
    user_introduction = serializers.CharField(required=False, help_text="用户介绍")
    nickname = serializers.CharField(required=False, help_text="昵称")

    class Meta:
        model = Account

        fields = ('username', 'password', 'email', 'user_introduction', 'nickname')


class UserRoleSerializer(BaseSerializer):
    """用户登录信息"""

    class Meta:
        model = UserRole

        # 定义需要返回的字段及顺序
        fields = ('user_role_id',
                  'user_id',
                  'user_name',
                  'user_token',
                  'create_tm_format',
                  'update_tm_format')


class UserDetailSerializer(serializers.ModelSerializer):
    """用户详情信息"""
    user_detail_id = serializers.CharField(read_only=True, help_text="用户详情ID")
    user_introduction = serializers.CharField(read_only=True, help_text="用户介绍")
    nickname = serializers.CharField(read_only=True, help_text="昵称")
    user_email = serializers.CharField(read_only=True, help_text="邮箱")
    user_id = serializers.IntegerField(required=True, help_text='用户ID')

    class Meta:
        model = UserDetail

        fields = ('user_detail_id',
                  'user_id',
                  'user_name',
                  'nickname',
                  'user_email',
                  'user_introduction')


class UserDisableSerializer(BaseSerializer):
    """用户禁用启用"""
    user_id = serializers.IntegerField(required=True, help_text='用户ID')
    is_disable = serializers.BooleanField(required=True, help_text='用户状态：1:启用；2:禁用')

    class Meta:
        model = Account

        fields = ('user_id', 'is_disable')
