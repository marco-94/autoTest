"""
用例管理的全部筛选器
"""
import django_filters
from module.module_list.models import ModuleList
from caseGroup.models import CaseGroupList


class CaseGroupListFilter(django_filters.rest_framework.FilterSet):
    case_group_id = django_filters.NumberFilter(field_name='case_group_id', lookup_expr='exact')
    module = django_filters.NumberFilter(field_name='module', lookup_expr='exact')
    case_group_name = django_filters.CharFilter(field_name='case_group_name', lookup_expr='icontains')
    case_group_desc = django_filters.CharFilter(field_name='case_group_desc', lookup_expr='icontains')
    created_start_tm = django_filters.DateTimeFromToRangeFilter(field_name='创建开始时间')
    created_end_tm = django_filters.DateTimeFromToRangeFilter(field_name='创建结束时间')

    class Meta:
        model = ModuleList
        fields = ('case_group_id', 'module', 'case_group_name', 'case_group_desc', 'created_start_tm', 'created_end_tm')
