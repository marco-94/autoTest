from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, mixins, generics
from django_filters import rest_framework
from rest_framework.response import Response
from autoTest.common.render_response import APIResponse
from rest_framework.permissions import IsAuthenticated
from autoTest.common.auth import CustomJsonToken
from project.project_list.models import ProjectList
from project.project_detail.models import ProjectDetail
from project.project_serializers import *
from project.project_filter import ProjectListFilter
from autoTest.common.search_time import SearchTime
from autoTest.common.render_response import CustomerRenderer
from autoTest.base.base_views import GetLoginUser
from rest_framework.viewsets import GenericViewSet
from rest_framework_jwt.settings import api_settings
from autoTest.common.set_version import SetVersion
from autoTest.common.global_configuration import global_id

jwt_decode_handler = api_settings.JWT_DECODE_HANDLER


# Create your views here.
class ProjectListView(mixins.ListModelMixin, generics.GenericAPIView):
    authentication_classes = [CustomJsonToken]
    permission_classes = (IsAuthenticated,)
    renderer_classes = [CustomerRenderer]

    queryset = ProjectList.objects.all().order_by("-created_tm")
    serializer_class = ProjectListSerializer
    filter_class = ProjectListFilter
    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)

    @swagger_auto_schema(tags=['项目'],
                         operation_id="ProjectList",
                         operation_summary='项目列表',
                         operation_description='时间段查询需要传时间戳',
                         responses={"400014": "参数错误", 200: serializer_class})
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
        if not is_disable:
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


class ProjectCreateViews(mixins.CreateModelMixin, GenericViewSet):
    authentication_classes = [CustomJsonToken]
    permission_classes = (IsAuthenticated,)

    queryset = ProjectList.objects.all()
    serializer_class = ProjectCreateSerializer
    filter_class = ProjectListFilter
    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)

    @swagger_auto_schema(tags=['项目'],
                         operation_id="ProjectCreate",
                         operation_summary='新增项目',
                         operation_description='项目名称必填且唯一',
                         responses={
                             400014: "参数错误",
                             400013: "请检查输入字段是否正确(必填字段、未定义字段)",
                             500001: "项目名称长度需要1到20位",
                             500002: "项目已存在",
                             500003: "项目创建失败",
                             200: "新增成功"
                         })
    def create(self, request, *args, **kwargs):
        """新增项目"""
        # 新增数据时，需要把入参同时存放到ProjectList和ProjectDetail表，故先把入参按照models定义，拆分成两个字典，非上述表字段，不处理
        project_dict = {}
        detail_dict = {}
        for item in request.data.items():
            if item[0] in [field.name for field in ProjectList._meta.get_fields()]:
                project_dict[item[0]] = item[1]
            elif item[0] in [field.name for field in ProjectDetail._meta.get_fields()]:
                detail_dict[item[0]] = item[1]

        # 获取当前登录用户信息
        user = GetLoginUser().get_login_user(request)
        if user["code"] == 200:
            project_dict["editor"] = user["username"]
        else:
            return Response(user)

        # 检查项目名称是否有填写
        if "project_name" not in list(project_dict.keys()):
            return APIResponse(400013, '请检查输入字段是否正确(必填字段、未定义字段)', success=False)
        else:
            if len(project_dict["project_name"]) > 20 or len(project_dict["project_name"]) < 1:
                return APIResponse(500001, '项目名称长度需要1到20位', success=False)

        project_name = project_dict["project_name"]
        try:
            ProjectList.objects.get(project_name=project_name)
            return APIResponse(500002, '项目已存在', success=False)
        except ProjectList.DoesNotExist:
            try:
                project_create = ProjectList.objects.create(**project_dict)
                if project_create:
                    project_id = ProjectList.objects.filter(project_name=str(project_name)).values('project_id').first()
                    ProjectDetail.objects.update_or_create(defaults=detail_dict,
                                                           project_info_id=project_id["project_id"])
                    return APIResponse(200, '项目创建成功')
            except Exception:
                return APIResponse(500003, '项目创建失败', success=False)


class ProjectEditViews(mixins.UpdateModelMixin, generics.GenericAPIView):
    authentication_classes = [CustomJsonToken]
    permission_classes = (IsAuthenticated,)

    queryset = ProjectList.objects.all()
    serializer_class = ProjectEditSerializer
    filter_class = ProjectListFilter
    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)

    @swagger_auto_schema(tags=['项目'],
                         operation_id="ProjectEdit",
                         operation_summary='项目编辑',
                         operation_description='项目名称唯一',
                         responses={
                             400014: "参数错误",
                             400013: "请检查输入字段是否正确(必填字段、未定义字段)",
                             500001: "项目名称长度需要1到20位",
                             500002: "项目名称已存在",
                             500004: "项目不存在",
                             500005: "项目修改失败",
                             200: serializer_class
                         })
    def put(self, request, *args, **kwargs):
        """新增项目"""
        # 修改数据时，需要把入参同时存放到ProjectList和ProjectDetail表，故先把入参按照models定义，拆分成两个字典，非上述表字段，不处理
        project_dict = {}
        detail_dict = {}
        for item in request.data.items():
            if item[0] in [field.name for field in ProjectList._meta.get_fields()]:
                project_dict[item[0]] = item[1]
            elif item[0] in [field.name for field in ProjectDetail._meta.get_fields()]:
                detail_dict[item[0]] = item[1]

        # 获取当前登录用户信息
        user = GetLoginUser().get_login_user(request)
        if user["code"] == 200:
            project_dict["editor"] = user["username"]
        else:
            return Response(user)

        # 检查项目名称是否有填写
        if "project_name" not in list(project_dict.keys()):
            return APIResponse(400013, '请检查输入字段是否正确(必填字段、未定义字段)', success=False)
        else:
            if len(project_dict["project_name"]) > 20 or len(project_dict["project_name"]) < 1:
                return APIResponse(500001, '项目名称长度需要1到20位', success=False)

        # 非当前修改数据条件下，判断名称是否存在
        if ProjectList.objects.filter(project_name=project_dict["project_name"]).count() > 0:
            project_info = ProjectList.objects.filter(project_name=project_dict["project_name"]).values('project_id')
            # 查询到的同名数据ID与当前修改数据ID不一致时，不允许修改
            if not str(project_info[0]["project_id"]) == str(project_dict['project_id']):
                return APIResponse(500002, '项目名称已存在', success=False)

        project = ProjectList.objects.filter(project_id=project_dict['project_id'])
        if project:
            try:
                project_version = project.values("project_version").first()["project_version"]
                project_dict["project_version"] = SetVersion.model_version(project_version)
                project_update = project.update_or_create(defaults=project_dict, project_id=project_dict['project_id'])
                if project_update:
                    ProjectDetail.objects.update_or_create(defaults=detail_dict, project_info_id=project_dict['project_id'])
                    return APIResponse(200, '项目修改成功')
            except Exception:
                return APIResponse(500005, '项目修改失败', success=False)
        else:
            return APIResponse(500005, '项目不存在', success=False)


class ProjectDisableView(mixins.UpdateModelMixin, generics.GenericAPIView):
    authentication_classes = [CustomJsonToken]
    permission_classes = (IsAuthenticated,)

    queryset = ProjectList.objects.all()
    serializer_class = ProjectDisableSerializer

    @swagger_auto_schema(tags=["项目"],
                         operation_id="ProjectDisable",
                         operation_summary='项目禁用启用',
                         operation_description='1/false：启用；2/true：禁用',
                         responses={500004: "项目不存在",
                                    500006: "操作失败，项目状态不正确",
                                    200: "操作成功"})
    def put(self, request, *args, **kwargs):
        try:
            project_id = request.data.get('project_id')
            is_disable = request.data.get('is_disable')
        except Exception:
            return APIResponse(400014, '参数错误', success=False)

        if is_disable == 1:
            is_disable = False
        elif is_disable == 2:
            is_disable = True
        else:
            return APIResponse(400014, '参数错误', success=False)

        try:
            ProjectList.objects.get(project_id=project_id)
        except ProjectList.DoesNotExist:
            return APIResponse(500004, '项目不存在', success=False)

        try:
            ProjectList.objects.filter(project_id=project_id).get(is_disable=is_disable)
            return APIResponse(500006, '操作失败，项目状态不正确', success=False)
        except ProjectList.DoesNotExist:
            project = ProjectList.objects.filter(project_id=project_id).first()
            if project:
                ProjectList.objects.update_or_create(defaults={'is_disable': is_disable}, project_id=project_id)
                return APIResponse(200, '操作成功')
        return APIResponse(200, '操作成功')
