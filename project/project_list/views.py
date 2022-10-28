from drf_yasg.utils import swagger_auto_schema
from jwt import ExpiredSignatureError
from rest_framework import filters, mixins, generics
from rest_framework.generics import GenericAPIView
from django_filters import rest_framework
from rest_framework.response import Response

from autoTest.common.render_response import APIResponse
from rest_framework.permissions import IsAuthenticated
from autoTest.common.auth import CustomJsonToken
from project.project_list.models import ProjectList
from project.project_serializers import ProjectListSerializer
from project.project_filter import ProjectListFilter
from autoTest.common.search_time import SearchTime
from autoTest.common.render_response import CustomerRenderer
from autoTest.base.base_views import GetLoginUser
from rest_framework.viewsets import GenericViewSet
from rest_framework_jwt.settings import api_settings

jwt_decode_handler = api_settings.JWT_DECODE_HANDLER


# Create your views here.
class ProjectListView(mixins.ListModelMixin, generics.GenericAPIView):
    authentication_classes = [CustomJsonToken]
    permission_classes = (IsAuthenticated,)
    renderer_classes = [CustomerRenderer]

    queryset = ProjectList.objects.filter(is_delete=False).all().order_by("-created_tm")
    serializer_class = ProjectListSerializer
    filter_class = ProjectListFilter
    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)

    @swagger_auto_schema(tags=['项目'],
                         operation_summary='项目列表',
                         operation_description='时间段查询需要传时间戳',
                         responses={"400014": "参数错误"})
    def post(self, request, *args, **kwargs):
        """项目列表信息 """
        try:
            project_id = request.data.get("project_id")
            project_name = request.data.get("project_name")
            is_disable = request.data.get("is_disable")
            editor = request.data.get("editor")
            created_start_time = request.data.get('created_start_tm')
            created_end_time = request.data.get('created_end_tm')
            page = request.data.get('page')
            size = request.data.get('size')
        except Exception:
            return APIResponse(400014, '参数错误', success=False)

        if page:  # 判断请求中是否有page和size参数
            request.query_params._mutable = True  # 让查询参数dict变为可编辑
            # query_params该参数会返回请求的查询参数，是个dict _mutable属性表示是否可编辑，默认是False
            request.query_params['page'] = page  # 添加page查询参数
            if size:
                request.query_params['size'] = size  # 添加size查询参数
            request.query_params._mutable = False  # 让查询参数dict变为不可编辑

        # 查询入参集合
        search_dict = {}

        if project_id:
            search_dict["project_id"] = project_id
        if project_name:
            search_dict["project_name__icontains"] = project_name
        if editor:
            search_dict["editor__icontains"] = editor
        if is_disable:
            search_dict["is_disable"] = 1
        else:
            search_dict["is_disable"] = 0

        # 入参时间格式化
        if created_start_time and created_end_time:
            SearchTime().search_time_conversion(created_start_time, created_end_time, search_dict)

        # 由于覆盖了list方法，导致丢失了分页返回，故加上分页返回
        page_queryset = self.paginate_queryset(queryset=self.queryset.filter(**search_dict))

        # post请求加上分页条件查询
        if page_queryset is not None:
            serializer = self.get_serializer(page_queryset, many=True)
            return self.get_paginated_response(serializer.data)

        serializer_data = self.get_serializer(instance=page_queryset, many=True)

        return self.get_paginated_response(serializer_data.data)


class AddProjectViews(mixins.CreateModelMixin, GenericViewSet):
    # authentication_classes = [CustomJsonToken]
    # permission_classes = (IsAuthenticated,)
    authentication_classes = []
    permission_classes = ()

    queryset = ProjectList.objects.filter(is_delete=False).all().order_by("-created_tm")
    serializer_class = ProjectListSerializer
    filter_class = ProjectListFilter
    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)

    def create(self, request, *args, **kwargs):
        """新增项目"""
        try:
            # token = request.META.get('HTTP_AUTHORIZATION')
            project_name = request.data.get("project_name")
            project_desc = request.data.get("project_desc")
        except Exception:
            return APIResponse(400014, '参数错误', success=False)

        field_list = {}
        if project_name:
            field_list["project_name"] = project_name
        if project_desc:
            field_list["project_desc"] = project_desc

        # 获取当前登录用户信息
        user = GetLoginUser().get_login_user(request)
        if user["code"] == 200:
            field_list["editor"] = user["username"]
        else:
            return Response(user)

        # 检查账号密码是否有填写
        if "project_name" not in list(field_list.keys()):
            return APIResponse(400013, '请检查输入字段是否正确(必填字段、未定义字段)', success=False)
        else:
            if len(field_list["project_name"]) > 20 or len(field_list["project_name"]) < 1:
                return APIResponse(500001, '项目名称长度需要1到20位', success=False)

        try:
            ProjectList.objects.get(project_name=field_list["project_name"])
            return APIResponse(500002, '项目已存在', success=False)
        except ProjectList.DoesNotExist:
            try:
                ProjectList.objects.create(**field_list)
                return APIResponse(200, '项目创建成功')
            except Exception as e:
                print(e)
                return APIResponse(500003, '项目创建失败', success=False)
