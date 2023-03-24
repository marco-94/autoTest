"""
模块管理的全部筛选器
"""
import django_filters
from module.module_list.models import ModuleList
from module.module_detail.models import ModuleDetail


class ModuleListFilter(django_filters.rest_framework.FilterSet):
    module_id = django_filters.NumberFilter(field_name='module_id', lookup_expr='exact')
    belong_project = django_filters.NumberFilter(field_name='belong_project', lookup_expr='exact')
    module_name = django_filters.CharFilter(field_name='module_name', lookup_expr='icontains')
    module_desc = django_filters.CharFilter(field_name='module_desc', lookup_expr='icontains')
    created_start_tm = django_filters.DateTimeFromToRangeFilter(field_name='创建开始时间')
    created_end_tm = django_filters.DateTimeFromToRangeFilter(field_name='创建结束时间')

    class Meta:
        model = ModuleList
        fields = ('module_id', 'belong_project', 'module_name', 'module_desc', 'created_start_tm', 'created_end_tm')


class ModuleDetailFilter(django_filters.rest_framework.FilterSet):
    module_id = django_filters.NumberFilter(field_name='module_id', lookup_expr='exact')
    module_img = django_filters.CharFilter(field_name='module_img')
    module_url = django_filters.CharFilter(field_name='module_url')

    class Meta:
        model = ModuleDetail
        fields = '__all__'
