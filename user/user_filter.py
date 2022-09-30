"""
用户管理的全部筛选器
"""
import django_filters
from user.user_list.models import Account, UserRole
from user.user_detail.models import UserDetail


class UserFilter(django_filters.rest_framework.FilterSet):
    user_id = django_filters.NumberFilter(field_name='user_id', lookup_expr='exact')
    username = django_filters.CharFilter(field_name='username', lookup_expr='icontains')
    created_start_tm = django_filters.DateTimeFromToRangeFilter(field_name='创建开始时间')
    created_end_tm = django_filters.DateTimeFromToRangeFilter(field_name='创建结束时间')

    class Meta:
        model = Account
        fields = ('user_id', 'username', 'email', 'created_start_tm', 'created_end_tm')


class UserRoleFilter(django_filters.rest_framework.FilterSet):
    user_id = django_filters.NumberFilter(field_name='user_id', lookup_expr='exact')
    user_token = django_filters.CharFilter(field_name='user_token', lookup_expr='icontains')

    class Meta:
        model = UserRole
        fields = '__all__'


class UserDetailFilter(django_filters.rest_framework.FilterSet):
    user_id = django_filters.NumberFilter(field_name='user_id', lookup_expr='exact')
    nickname = django_filters.CharFilter(field_name='nickname', lookup_expr='icontains')

    class Meta:
        model = UserDetail
        fields = '__all__'
