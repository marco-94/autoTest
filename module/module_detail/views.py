from rest_framework import filters, mixins, generics
from django_filters import rest_framework
from autoTest.common.render_response import APIResponse
from rest_framework.permissions import IsAuthenticated
from autoTest.common.auth import CustomJsonToken
from module.module_detail.models import ModuleDetail
from module.module_serializers import ModuleDetailSerializer
from module.module_filter import ModuleDetailFilter
from drf_yasg.utils import swagger_auto_schema


class ModuleDetailView(mixins.ListModelMixin, generics.GenericAPIView):
    authentication_classes = (CustomJsonToken,)
    permission_classes = (IsAuthenticated,)
    queryset = ModuleDetail.objects.filter().all()
    serializer_class = ModuleDetailSerializer
    filter_class = ModuleDetailFilter
    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)

    @swagger_auto_schema(tags=['模块'],
                         operation_id="ModuleDetail",
                         operation_summary='模块详情',
                         operation_description='模块id必填',
                         responses={
                             400014: "参数错误",
                             600004: "模块不存在",
                             40013: "请检查输入字段是否正确(必填字段、未定义字段)",
                             200: serializer_class})
    def post(self, request, *args, **kwargs):
        """
        post: 用户详情信息

        user_id为精确传参

        40013：请检查输入字段是否正确

        40014：参数错误
        """
        try:
            module_id = request.data.get("module_id")
        except Exception:
            return APIResponse(40014, '参数错误', success=False)

        if module_id:
            try:
                module = ModuleDetail.objects.filter(module_info_id=module_id).first()
                if module:
                    module_data = ModuleDetail.objects.get(module_info_id=module_id)
                    serializer_data = ModuleDetailSerializer(module_data)
                    return APIResponse(200, '查询成功', success=True, data=serializer_data.data)
                return APIResponse(600004, '模块不存在', success=False)
            except ValueError:
                return APIResponse(40014, '参数错误', success=False)
        else:
            return APIResponse(40013, '请检查输入字段是否正确(必填字段、未定义字段)', success=False)
