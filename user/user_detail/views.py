from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import filters
from django_filters import rest_framework
from user.user_detail.models import UserDetail
from user import user_filter, user_serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from autoTest.common.auth import CustomJsonToken


# Create your views here.
class UserDetailView(viewsets.ModelViewSet):
    """用户详情信息"""
    authentication_classes = (CustomJsonToken,)
    permission_classes = (IsAuthenticated,)
    queryset = UserDetail.objects.filter().all()
    serializer_class = user_serializers.UserDetailSerializer
    filter_class = user_filter.UserDetailFilter
    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    ordering = ['-created_tm']

