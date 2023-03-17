"""
用户管理的全部序列化器
"""
from rest_framework import serializers
from user.user_list.models import Account, UserRole
from user.user_detail.models import UserDetail
from autoTest.base.base_serializers import BaseSerializer


class LoginSerializer(serializers.ModelSerializer):
    """登录入参序列化器"""
    user_id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)

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


class UserListSerializer(BaseSerializer):
    """用户基本信息"""
    user_id = serializers.IntegerField(required=False)
    is_disable = serializers.BooleanField(required=False)
    username = serializers.CharField(required=False)
    user_introduction = serializers.CharField(read_only=True)
    nickname = serializers.CharField(read_only=True)
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

    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    email = serializers.CharField(required=False)
    user_introduction = serializers.CharField(required=False)
    nickname = serializers.CharField(required=False)

    class Meta:
        model = Account

        fields = ('username', 'password', 'email', 'user_introduction', 'nickname')


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


class UserDetailSerializer(serializers.ModelSerializer):
    """用户详情信息"""
    user_introduction = serializers.CharField(read_only=True)
    nickname = serializers.CharField(read_only=True)
    user_email = serializers.CharField(read_only=True)
    user_id = serializers.IntegerField(required=True, help_text='用户ID')

    class Meta:
        model = UserDetail

        fields = ('id',
                  'user_id',
                  'user_name',
                  'nickname',
                  'user_email',
                  'user_introduction')


class UserDisableSerializer(BaseSerializer):
    """用户禁用启用"""
    user_id = serializers.IntegerField(required=True, help_text='用户ID')
    is_disable = serializers.BooleanField(required=True, help_text='0:启用；1:禁用')

    class Meta:
        model = Account

        fields = ('user_id', 'is_disable')
