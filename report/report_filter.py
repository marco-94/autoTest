"""
报告管理的全部筛选器
"""
import django_filters
from report.report_list.models import ReportList


class ReportListFilter(django_filters.rest_framework.FilterSet):
    report_id = django_filters.NumberFilter(field_name='report_id', lookup_expr='exact')
    report_name = django_filters.CharFilter(field_name='report_name', lookup_expr='icontains')
    report_desc = django_filters.CharFilter(field_name='report_desc', lookup_expr='icontains')
    created_start_tm = django_filters.DateTimeFromToRangeFilter(field_name='创建开始时间')
    created_end_tm = django_filters.DateTimeFromToRangeFilter(field_name='创建结束时间')

    class Meta:
        model = ReportList
        fields = ('report_id', 'report_name', 'report_desc', 'created_start_tm', 'created_end_tm')
