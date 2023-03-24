"""
用例管理的全部筛选器
"""
import django_filters
from case.case_list.models import CaseList


class CaseListFilter(django_filters.rest_framework.FilterSet):
    case_id = django_filters.NumberFilter(field_name='case_id', lookup_expr='exact')
    case_group = django_filters.NumberFilter(field_name='case_group', lookup_expr='exact')
    module = django_filters.NumberFilter(field_name='module', lookup_expr='exact')
    project = django_filters.NumberFilter(field_name='project', lookup_expr='exact')
    case_name = django_filters.CharFilter(field_name='case_name', lookup_expr='icontains')
    case_desc = django_filters.CharFilter(field_name='case_desc', lookup_expr='icontains')
    created_start_tm = django_filters.DateTimeFromToRangeFilter(field_name='创建开始时间')
    created_end_tm = django_filters.DateTimeFromToRangeFilter(field_name='创建结束时间')

    class Meta:
        model = CaseList
        fields = ('case_id',
                  'case_group',
                  'module',
                  'project',
                  'case_name',
                  'case_desc',
                  'created_start_tm',
                  'created_end_tm')
