"""
模块管理的全部序列化器
"""
from rest_framework import serializers
from project.project_list.models import ProjectList
from module.module_list.models import ModuleList
from module.module_detail.models import ModuleDetail
from autoTest.base.base_serializers import BaseSerializer


class ModuleListSerializer(BaseSerializer):
    module_id = serializers.IntegerField(required=False, help_text='模块ID')

    # 设置只读只写
    is_disable = serializers.BooleanField(read_only=True, help_text='是否禁用(0：启用，1：禁用)')
    belong_project = serializers.SlugRelatedField(queryset=ProjectList.objects.all(),
                                                  slug_field="project_id",
                                                  required=True,
                                                  help_text='所属项目ID')
    # 设置非必填
    module_desc = serializers.CharField(required=False, help_text='模块描述')
    module_name = serializers.CharField(required=True, help_text='模块名称')
    editor = serializers.CharField(required=False, help_text='创建人/更新人')
    module_version = serializers.CharField(read_only=True, required=False, help_text='模块版本')

    class Meta:
        model = ModuleList

        fields = ('module_id',
                  'module_name',
                  'module_version',
                  'belong_project',
                  'created_start_tm',
                  'created_end_tm',
                  'is_disable',
                  'module_desc',
                  'editor',
                  "created_tm",
                  "updated_tm",
                  "create_tm_format",
                  "update_tm_format"
                  )


class ModuleDetailSerializer(serializers.ModelSerializer):
    """模块详情信息"""
    module_id = serializers.IntegerField(required=True, help_text='模块ID')
    module_img = serializers.CharField(read_only=True, help_text='模块图片')
    module_url = serializers.CharField(read_only=True, help_text='模块链接')

    class Meta:
        model = ModuleDetail

        fields = ('module_id',
                  'module_detail_id',
                  'module_name',
                  'module_desc',
                  'module_img',
                  'module_url',
                  'editor',)


class ModuleEditSerializer(BaseSerializer):
    """编辑模块信息"""
    module_id = serializers.IntegerField(required=True, help_text='模块ID')
    module_desc = serializers.CharField(required=False, help_text='模块描述')
    module_name = serializers.CharField(required=True, help_text='模块名称')

    class Meta:
        model = ModuleDetail

        fields = ('module_id',
                  'module_name',
                  'module_desc',
                  'editor',)


class ModuleDisableSerializer(BaseSerializer):
    """模块禁用启用"""
    module_id = serializers.IntegerField(required=True, help_text='模块ID')
    is_disable = serializers.BooleanField(required=True, help_text='1:启用；2:禁用')

    class Meta:
        model = ModuleList

        fields = ('module_id', 'is_disable')
