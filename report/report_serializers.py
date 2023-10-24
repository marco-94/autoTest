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

        fields = ('report_id',
                  'report_name',
                  'created_start_tm',
                  'created_end_tm',
                  'report_desc',
                  'editor',
                  'case',
                  'group',
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
