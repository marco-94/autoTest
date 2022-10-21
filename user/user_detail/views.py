from django_filters import rest_framework
from rest_framework import filters, mixins, generics
from rest_framework.viewsets import GenericViewSet
from user.user_detail.models import UserDetail
from user import user_filter, user_serializers
from rest_framework.permissions import IsAuthenticated
from autoTest.common.auth import CustomJsonToken
from autoTest.common.render_response import APIResponse


# Create your views here.
class UserDetailView(mixins.ListModelMixin, GenericViewSet):
    """
    list: 用户详情信息

    " "
    """
    authentication_classes = (CustomJsonToken,)
    permission_classes = (IsAuthenticated,)
    queryset = UserDetail.objects.filter().all()
    serializer_class = user_serializers.UserDetailSerializer
    filter_class = user_filter.UserDetailFilter
    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    ordering = ['-created_tm']


class UserDetailViewV2(mixins.ListModelMixin, generics.GenericAPIView):
    authentication_classes = (CustomJsonToken,)
    permission_classes = (IsAuthenticated,)
    queryset = UserDetail.objects.filter().all().order_by('-created_tm')
    serializer_class = user_serializers.UserDetailSerializer
    filter_class = user_filter.UserDetailFilter
    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)

    def post(self, request, *args, **kwargs):
        """
        post: 用户详情信息

        user_id为精确传参

        40013：请检查输入字段是否正确

        40014：参数错误
        """
        try:
            user_id = request.data.get("user_id")
        except Exception:
            return APIResponse(40014, '参数错误', success=False)

        if user_id:
            try:
                page_queryset = self.paginate_queryset(queryset=self.queryset.filter(user_info_id=user_id))

                serializer_data = self.get_serializer(instance=page_queryset, many=True)

                return self.get_paginated_response(serializer_data.data)
            except ValueError:
                return APIResponse(40014, '参数错误', success=False)
        else:
            return APIResponse(40013, '请检查输入字段是否正确(必填字段、未定义字段)', success=False)


