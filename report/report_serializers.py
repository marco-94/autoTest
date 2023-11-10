"""
报告管理的全部序列化器
"""
from rest_framework import serializers
from report.report_list.models import ReportList
from case.case_list.models import CaseList
from caseGroup.models import CaseGroupList
from autoTest.base.base_serializers import BaseSerializer


class ReportListSerializer(BaseSerializer):
    report_id = serializers.IntegerField(required=False, help_text='报告ID')

    # 设置非必填
    report_desc = serializers.CharField(required=False, help_text='报告描述')
    report_name = serializers.CharField(required=False, help_text='报告名称')
    editor = serializers.CharField(required=False, help_text='创建人/更新人')
    case_group_id = serializers.IntegerField(read_only=True, source="group.case_group_id", help_text='所属用例组ID')
    case_group_name = serializers.CharField(read_only=True, source="group.case_group_name", help_text='所属用例组名称')
    case_group = serializers.CharField(write_only=True, required=False, help_text='所属用例组')
    case_id = serializers.IntegerField(read_only=True, source="case.case_id", help_text='所属用例ID')
    case_name = serializers.CharField(read_only=True, source="case.case_name", help_text='所属用例名称')
    case = serializers.CharField(write_only=True, required=False, help_text='所属用例')

    class Meta:
        model = ReportList

        fields = ('report_id',
                  'report_name',
                  'created_start_tm',
                  'created_end_tm',
                  'report_desc',
                  'editor',
                  'case',
                  'case_id',
                  'case_name',
                  'case_group',
                  'case_group_id',
                  'case_group_name',
                  "created_tm",
                  "updated_tm",
                  "create_tm_format",
                  "update_tm_format"
                  )

    class ReportCreateSerializer(BaseSerializer):
        report_desc = serializers.CharField(required=False, help_text='报告描述')

        report_name = serializers.CharField(required=True, help_text='报告名称')
        editor = serializers.CharField(required=True, help_text='创建人')

        case = serializers.SlugRelatedField(queryset=CaseList.objects.all(),
                                            slug_field="case_id",
                                            required=False,
                                            help_text='所属用例ID')

        group = serializers.SlugRelatedField(queryset=CaseGroupList.objects.all(),
                                             slug_field="case_group_id",
                                             required=False,
                                             help_text='所属用例组ID')

        class Meta:
            model = ReportList

            fields = ('case_name',
                      'case',
                      'editor',
                      'group',
                      'case_desc',
                      )
