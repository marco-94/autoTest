from rest_framework import filters, mixins, generics
from django_filters import rest_framework
from autoTest.common.render_response import APIResponse
from rest_framework.permissions import IsAuthenticated
from autoTest.common.auth import CustomJsonToken
from project.project_detail.models import ProjectDetail
from project.project_serializers import ProjectDetailSerializer
from project.project_filter import ProjectDetailFilter
from drf_yasg.utils import swagger_auto_schema


class ProjectDetailView(mixins.ListModelMixin, generics.GenericAPIView):
    authentication_classes = (CustomJsonToken,)
    permission_classes = (IsAuthenticated,)
    queryset = ProjectDetail.objects.filter().all()
    serializer_class = ProjectDetailSerializer
    filter_class = ProjectDetailFilter
    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)

    @swagger_auto_schema(tags=['项目'],
                         operation_id="ProjectDetail",
                         operation_summary='项目详情',
                         operation_description='项目id必填',
                         responses={
                             400014: "参数错误",
                             500004: "项目不存在",
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
            project_id = request.data.get("project_id")
        except Exception:
            return APIResponse(40014, '参数错误', success=False)

        if project_id:
            try:
                project = ProjectDetail.objects.filter(project_info_id=project_id).first()
                if project:
                    project_data = ProjectDetail.objects.get(project_info_id=project_id)
                    serializer_data = ProjectDetailSerializer(project_data)
                    return APIResponse(200, '查询成功', success=True, data=serializer_data.data)
                return APIResponse(500004, '项目不存在', success=False)
            except ValueError:
                return APIResponse(40014, '参数错误', success=False)
        else:
            return APIResponse(40013, '请检查输入字段是否正确(必填字段、未定义字段)', success=False)