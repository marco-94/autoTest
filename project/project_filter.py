"""
项目管理的全部筛选器
"""
import django_filters
from project.project_list.models import ProjectList
from project.project_detail.models import ProjectDetail


class ProjectListFilter(django_filters.rest_framework.FilterSet):
    project_id = django_filters.NumberFilter(field_name='project_id', lookup_expr='exact')
    project_name = django_filters.CharFilter(field_name='project_name', lookup_expr='icontains')
    project_desc = django_filters.CharFilter(field_name='project_desc', lookup_expr='icontains')
    created_start_tm = django_filters.DateTimeFromToRangeFilter(field_name='创建开始时间')
    created_end_tm = django_filters.DateTimeFromToRangeFilter(field_name='创建结束时间')

    class Meta:
        model = ProjectList
        fields = ('project_id', 'project_name', 'project_desc', 'created_start_tm', 'created_end_tm')


class ProjectDetailFilter(django_filters.rest_framework.FilterSet):
    project_id = django_filters.NumberFilter(field_name='project_id', lookup_expr='exact')
    project_img = django_filters.CharFilter(field_name='project_img')
    project_url = django_filters.CharFilter(field_name='project_url')

    class Meta:
        model = ProjectDetail
        fields = '__all__'
