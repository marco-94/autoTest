"""
用例管理的全部序列化器
"""
from rest_framework import serializers
from case.case_list.models import CaseList
from caseGroup.models import CaseGroupList
from module.module_list.models import ModuleList
from project.project_list.models import ProjectList
from autoTest.base.base_serializers import BaseSerializer


class CaseListSerializer(BaseSerializer):
    case_id = serializers.IntegerField(required=False, help_text='用例ID')

    is_disable = serializers.BooleanField(read_only=True, help_text='是否禁用(0：启用，1：禁用)')

    case_group_id = serializers.IntegerField(read_only=True, source="group.case_group_id", help_text='所属用例组ID')
    case_group_name = serializers.CharField(read_only=True, source="group.case_group_name", help_text='所属用例组名称')
    case_group = serializers.CharField(write_only=True, required=False, help_text='所属用例组')

    module_id = serializers.IntegerField(read_only=True, source='module.module_id', help_text='所属模块ID')
    module_name = serializers.CharField(read_only=True, source='module.module_name', help_text='所属模块名称')
    module = serializers.CharField(write_only=True, required=False, help_text='所属模块')

    project_id = serializers.IntegerField(read_only=True, source='project.project_id', help_text='所属项目ID')
    project_name = serializers.CharField(read_only=True, source='project.project_name', help_text='所属项目名称')
    project = serializers.CharField(write_only=True, required=False, help_text='所属项目')
    # 设置非必填
    case_desc = serializers.CharField(required=False, help_text='用例描述')
    case_name = serializers.CharField(required=False, help_text='用例名称')
    editor = serializers.CharField(required=False, help_text='创建人/更新人')
    case_version = serializers.CharField(read_only=True, required=False, help_text='用例版本')

    class Meta:
        model = CaseList

        fields = ('case_id',
                  'case_name',
                  'case_version',
                  'case_group',
                  'case_group_id',
                  'case_group_name',
                  'module',
                  'module_id',
                  'module_name',
                  'project',
                  'project_id',
                  'project_name',
                  'created_start_tm',
                  'created_end_tm',
                  'is_disable',
                  'case_desc',
                  'editor',
                  "created_tm",
                  "updated_tm",
                  "create_tm_format",
                  "update_tm_format"
                  )


class CaseCreateSerializer(BaseSerializer):
    case_desc = serializers.CharField(required=False, help_text='用例描述')

    case_name = serializers.CharField(required=True, help_text='用例名称')

    group = serializers.SlugRelatedField(queryset=CaseGroupList.objects.all(),
                                         slug_field="case_group_id",
                                         required=True,
                                         help_text='所属用例组ID')

    class Meta:
        model = CaseList

        fields = ('case_name',
                  'group',
                  'case_desc',
                  )


class CaseEditSerializer(BaseSerializer):
    """编辑用例信息"""
    case_id = serializers.IntegerField(required=True, write_only=True, help_text='用例ID')
    case_desc = serializers.CharField(required=False, help_text='用例描述')
    case_name = serializers.CharField(required=True, help_text='用例名称')

    class Meta:
        model = CaseList

        fields = ('case_id',
                  'case_name',
                  'case_desc')


class CaseDisableSerializer(BaseSerializer):
    """用例禁用启用"""
    case_id = serializers.IntegerField(required=True, help_text='用例ID')
    is_disable = serializers.IntegerField(required=True, help_text='1:启用；2:禁用')

    class Meta:
        model = CaseList

        fields = ('case_id', 'is_disable')
