"""
项目管理的全部序列化器
"""
from rest_framework import serializers
from project.project_list.models import ProjectList
from autoTest.base.base_serializers import BaseSerializer


class ProjectListSerializer(BaseSerializer):
    project_id = serializers.IntegerField(required=False, help_text='项目ID')

    # 设置只读只写
    is_disable = serializers.BooleanField(read_only=True, help_text='是否禁用(0：启用，1：禁用)')

    # 设置非必填
    project_desc = serializers.CharField(required=False, help_text='项目描述')
    project_name = serializers.CharField(required=True, help_text='项目名称')
    editor = serializers.CharField(required=False, help_text='创建人/更新人')
    project_version = serializers.CharField(read_only=True, required=False, help_text='项目版本')

    class Meta:
        model = ProjectList

        fields = ('project_id',
                  'project_name',
                  'project_version',
                  'created_start_tm',
                  'created_end_tm',
                  'is_disable',
                  'project_desc',
                  'editor',
                  "created_tm",
                  "updated_tm",
                  "create_tm_format",
                  "update_tm_format"
                  )

