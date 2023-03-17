from django_filters import rest_framework
from rest_framework import filters, mixins, generics
from user.user_detail.models import UserDetail
from user import user_filter, user_serializers
from rest_framework.permissions import IsAuthenticated
from autoTest.common.auth import CustomJsonToken
from autoTest.common.render_response import APIResponse
from drf_yasg.utils import swagger_auto_schema
from autoTest.common.render_response import CustomerRenderer
from django.core import serializers
import json


# Create your views here.
class UserDetailView(mixins.ListModelMixin, generics.GenericAPIView):
    authentication_classes = (CustomJsonToken,)
    permission_classes = (IsAuthenticated,)
    # renderer_classes = [CustomerRenderer]
    queryset = UserDetail.objects.filter().all()
    serializer_class = user_serializers.UserDetailSerializer
    filter_class = user_filter.UserDetailFilter
    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)

    @swagger_auto_schema(tags=["用户"],
                         operation_id="UserDetail",
                         operation_summary='用户详情',
                         operation_description='',
                         responses={
                             400014: "参数错误",
                             40013: "请检查输入字段是否正确(必填字段、未定义字段)",
                             200: serializer_class
                         })
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
                user = UserDetail.objects.filter(user_info_id=user_id).first()
                if user:
                    user_data = UserDetail.objects.get(user_info_id=user_id)
                    serializers_data = user_serializers.UserDetailSerializer(user_data)
                    return APIResponse(200, '查询成功', success=True, data=serializers_data.data)
                return APIResponse(400001, '用户不存在', success=False)
            except ValueError:
                return APIResponse(40014, '参数错误', success=False)
        else:
            return APIResponse(40013, '请检查输入字段是否正确(必填字段、未定义字段)', success=False)


