"""
用例组管理的全部序列化器
"""
from rest_framework import serializers
from caseGroup.models import CaseGroupList
from module.module_list.models import ModuleList
from project.project_list.models import ProjectList
from autoTest.base.base_serializers import BaseSerializer


class CaseGroupListSerializer(BaseSerializer):
    case_group_id = serializers.IntegerField(required=False, help_text='用例组ID')

    # 设置只读只写
    is_disable = serializers.BooleanField(read_only=True, help_text='是否禁用(0：启用，1：禁用)')
    module = serializers.SlugRelatedField(queryset=ModuleList.objects.all(),
                                          slug_field="module_id",
                                          required=True,
                                          help_text='所属模块ID')

    project = serializers.SlugRelatedField(queryset=ProjectList.objects.all(),
                                           slug_field="project_id",
                                           required=True,
                                           help_text='所属项目ID')
    # 设置非必填
    case_group_desc = serializers.CharField(required=False, help_text='用例组描述')
    case_group_name = serializers.CharField(required=True, help_text='用例组名称')
    editor = serializers.CharField(required=False, help_text='创建人/更新人')
    case_group_version = serializers.CharField(read_only=True, required=False, help_text='用例组版本')

    class Meta:
        model = CaseGroupList

        fields = ('case_group_id',
                  'case_group_name',
                  'case_group_version',
                  'module',
                  'project',
                  'created_start_tm',
                  'created_end_tm',
                  'is_disable',
                  'case_group_desc',
                  'editor',
                  "created_tm",
                  "updated_tm",
                  "create_tm_format",
                  "update_tm_format"
                  )


class CaseGroupCreateSerializer(BaseSerializer):
    module = serializers.SlugRelatedField(queryset=ModuleList.objects.all(),
                                          slug_field="module_id",
                                          required=True,
                                          help_text='所属模块ID')
    project = serializers.SlugRelatedField(queryset=ProjectList.objects.all(),
                                           slug_field="project_id",
                                           required=True,
                                           help_text='所属项目ID')
    # 设置非必填
    case_group_desc = serializers.CharField(required=False, help_text='用例组描述')
    case_group_name = serializers.CharField(required=True, help_text='用例组名称')

    class Meta:
        model = CaseGroupList

        fields = ('case_group_name',
                  'module',
                  'project',
                  'case_group_desc',
                  )


class CaseGroupEditSerializer(BaseSerializer):
    """编辑用例组信息"""
    case_group_id = serializers.IntegerField(required=True, write_only=True, help_text='用例组ID')
    case_group_desc = serializers.CharField(required=False, help_text='用例组描述')
    case_group_name = serializers.CharField(required=True, help_text='用例组名称')

    class Meta:
        model = CaseGroupList

        fields = ('case_group_id',
                  'case_group_name',
                  'case_group_desc',
                  'editor',)


class CaseGroupDisableSerializer(BaseSerializer):
    """用例组禁用启用"""
    case_group_id = serializers.IntegerField(required=True, help_text='用例组ID')
    is_disable = serializers.BooleanField(required=True, help_text='1:启用；2:禁用')

    class Meta:
        model = CaseGroupList

        fields = ('case_group_id', 'is_disable')
