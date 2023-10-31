"""
模块管理的全部序列化器
"""
from rest_framework import serializers
from project.project_list.models import ProjectList
from module.module_list.models import ModuleList
from module.module_detail.models import ModuleDetail
from autoTest.base.base_serializers import BaseSerializer


class ModuleCreateSerializer(BaseSerializer):
    module_name = serializers.CharField(required=True, help_text='模块名称')
    module_desc = serializers.CharField(required=False, help_text='模块描述')
    module_img = serializers.CharField(required=False, help_text='模块图片')
    module_url = serializers.CharField(required=False, help_text='模块链接')
    belong_project = serializers.SlugRelatedField(queryset=ProjectList.objects.all(),
                                                  slug_field="project_id",
                                                  required=True,
                                                  help_text='所属项目ID')

    class Meta:
        model = ModuleList

        fields = ('module_name',
                  'belong_project',
                  'module_img',
                  'module_url',
                  'module_desc')


class ModuleListSerializer(BaseSerializer):
    module_id = serializers.IntegerField(required=False, help_text='模块ID')

    # 设置只读只写
    is_disable = serializers.BooleanField(required=False, help_text='是否禁用(0：启用，1：禁用)')
    project_id = serializers.IntegerField(read_only=True, required=False, source="belong_project.project_id",
                                          help_text='所属项目ID')
    project_name = serializers.CharField(read_only=True, required=False, source="belong_project.project_name",
                                         help_text='所属项目')
    project = serializers.CharField(write_only=True, required=False, help_text='所属项目')
    # belong_project = serializers.SlugRelatedField(queryset=ProjectList.objects.all(),
    #                                               slug_field="project_id",
    #                                               required=True,
    #                                               help_text='所属项目ID')
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
                  'project',
                  'project_id',
                  'project_name',
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


class ModuleDetailSerializer(BaseSerializer):
    """模块详情信息"""
    module_id = serializers.IntegerField(required=True, help_text='模块ID')
    module_detail_id = serializers.IntegerField(read_only=True, help_text='模块详情ID')
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
                  'editor',
                  "created_tm",
                  "updated_tm",
                  "create_tm_format",
                  "update_tm_format"
                  )


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
