"""
项目管理的全部序列化器
"""
from rest_framework import serializers
from project.project_list.models import ProjectList
from autoTest.base.base_serializers import BaseSerializer


class ProjectListSerializer(BaseSerializer):
    project_id = serializers.IntegerField(required=False)

    # 设置只读只写
    is_disable = serializers.BooleanField(read_only=True)

    # 设置非必填
    project_desc = serializers.CharField(required=False)
    project_name = serializers.CharField(required=False)
    editor = serializers.CharField(required=False)
    project_version = serializers.CharField(read_only=True, required=False)
    created_start_tm = serializers.IntegerField(write_only=True, required=False)
    created_end_tm = serializers.IntegerField(write_only=True, required=False)

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
                  "created_tm", "updated_tm", "create_tm_format", "update_tm_format"
                  )

