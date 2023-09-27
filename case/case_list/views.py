from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, mixins, generics
from django_filters import rest_framework
from rest_framework.response import Response
from autoTest.common.render_response import APIResponse
from rest_framework.permissions import IsAuthenticated
from autoTest.common.auth import CustomJsonToken
from module.module_list.models import ModuleList
from caseGroup.models import CaseGroupList
from case.case_list.models import *
from case.case_serializers import *
from case.case_filter import *
from autoTest.common.search_time import SearchTime
from autoTest.common.render_response import CustomerRenderer
from autoTest.base.base_views import GetLoginUser
from rest_framework.viewsets import GenericViewSet
from rest_framework_jwt.settings import api_settings
from autoTest.common.set_version import SetVersion

jwt_decode_handler = api_settings.JWT_DECODE_HANDLER


class CaseCreateViews(mixins.CreateModelMixin, GenericViewSet):
    authentication_classes = [CustomJsonToken]
    permission_classes = (IsAuthenticated,)

    queryset = CaseList.objects.all()
    serializer_class = CaseCreateSerializer
    filter_class = CaseListFilter
    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)

    @swagger_auto_schema(tags=['用例'],
                         operation_id="CaseCreate",
                         operation_summary='新增用例',
                         operation_description='用例名称必填且唯一',
                         responses={
                             400014: "参数错误",
                             600004: "项目不存在",
                             400013: "请检查输入字段是否正确(必填字段、未定义字段)",
                             800001: "用例名称长度需要1到20位",
                             800002: "用例已存在",
                             800003: "用例创建失败",
                             700004: "用例组不存在或已被禁用",
                             200: "新增成功"
                         })
    def create(self, request, *args, **kwargs):
        """新增用例"""
        # 新增数据时，筛选掉无用的入参
        case_dict = {}
        for item in request.data.items():
            if item[0] in [field.name for field in CaseList._meta.get_fields()]:
                case_dict[item[0]] = item[1]

        # 获取当前登录用户信息
        user = GetLoginUser().get_login_user(request)
        if user["code"] == 200:
            case_dict["editor"] = user["username"]
        else:
            return Response(user)
        # 检查用例名称和所属项目组是否有填写
        if "case_name" not in list(case_dict.keys()) or "group" not in list(case_dict.keys()):
            return APIResponse(400013, '请检查输入字段是否正确(必填字段、未定义字段)', success=False)
        else:
            if len(case_dict["case_name"]) > 20 or len(case_dict["case_name"]) < 1:
                return APIResponse(800001, '用例名称长度需要1到20位', success=False)

        # 更变字段名
        case_dict["group_id"] = case_dict.pop("group")

        try:
            CaseGroupList.objects.get(case_group_id=case_dict["group_id"], is_disable=False, is_delete=False)
            # 通过传入的用例组ID，在用例组列表找到对应的模块和项目ID
            case_group = CaseGroupList.objects.filter(case_group_id=case_dict["group_id"])
            module_id = case_group.values("module_id").first()["module_id"]
            project_id = case_group.values("project_id").first()["project_id"]
            case_dict["module_id"] = module_id
            case_dict["project_id"] = project_id

        except Exception:
            return APIResponse(700004, '用例组不存在或已被禁用', success=False)

        try:
            CaseList.objects.get(case_name=case_dict["case_name"])
            return APIResponse(800002, '用例已存在', success=False)
        except CaseList.DoesNotExist:
            try:
                CaseList.objects.create(**case_dict)
                return APIResponse(200, '用例创建成功')
            except Exception:
                return APIResponse(800003, '用例创建失败', success=False)


class CaseListView(mixins.ListModelMixin, generics.GenericAPIView):
    authentication_classes = [CustomJsonToken]
    permission_classes = (IsAuthenticated,)
    renderer_classes = [CustomerRenderer]

    queryset = CaseList.objects.all().order_by("-created_tm")
    serializer_class = CaseListSerializer
    filter_class = CaseListFilter
    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)

    @swagger_auto_schema(tags=['用例'],
                         operation_id="CaseList",
                         operation_summary='用例列表',
                         operation_description='时间段查询需要传时间戳',
                         responses={"400014": "参数错误", 200: serializer_class})
    def post(self, request, *args, **kwargs):
        """用例列表信息 """
        try:
            case_id = request.data.get("case_id")
            module_id = request.data.get("module_id")
            case_name = request.data.get("case_name")
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

        if case_id:
            search_dict["case_id"] = case_id
        if module_id:
            search_dict["module_id"] = module_id
        if case_name:
            search_dict["case_name__icontains"] = case_name
        if editor:
            search_dict["editor__icontains"] = editor
        if is_disable:
            search_dict["is_disable"] = 1
        if "is_disable" in search_dict and not is_disable:
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


class CaseEditViews(mixins.UpdateModelMixin, generics.GenericAPIView):
    authentication_classes = [CustomJsonToken]
    permission_classes = (IsAuthenticated,)

    queryset = CaseList.objects.all()
    serializer_class = CaseEditSerializer
    filter_class = CaseListFilter
    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)

    @swagger_auto_schema(tags=['用例'],
                         operation_id="CaseEdit",
                         operation_summary='用例编辑',
                         operation_description='用例名称唯一',
                         responses={
                             400014: "参数错误",
                             400013: "请检查输入字段是否正确(必填字段、未定义字段)",
                             800001: "用例名称长度需要1到20位",
                             800002: "用例名称已存在",
                             800004: "用例不存在",
                             800005: "用例修改失败",
                             200: serializer_class
                         })
    def put(self, request, *args, **kwargs):
        """编辑用例组"""
        # 修改数据时，需要把入参同时存放到列表和详情两个表，故先把入参按照models定义，拆分成两个字典，非上述表字段，不处理
        case_dict = {}
        for item in request.data.items():
            if item[0] in [field.name for field in CaseList._meta.get_fields()]:
                case_dict[item[0]] = item[1]

        # 获取当前登录用户信息
        user = GetLoginUser().get_login_user(request)
        if user["code"] == 200:
            case_dict["editor"] = user["username"]
        else:
            return Response(user)

        # 检查用例组名称是否有填写
        if "case_id" not in list(case_dict.keys()) or "case_name" not in list(case_dict.keys()):
            return APIResponse(400013, '请检查输入字段是否正确(必填字段、未定义字段)', success=False)
        else:
            if len(case_dict["case_name"]) > 20 or len(case_dict["case_name"]) < 1:
                return APIResponse(800001, '用例名称长度需要1到20位', success=False)

        # 非当前修改数据条件下，判断名称是否存在
        if CaseList.objects.filter(case_name=case_dict["case_name"]).count() > 0:
            case_info = CaseList.objects.filter(case_name=case_dict["case_name"]).values('case_id')
            # 查询到的同名数据ID与当前修改数据ID不一致时，不允许修改
            if not str(case_info[0]["case_id"]) == str(case_dict['case_id']):
                return APIResponse(800002, '用例名称已存在', success=False)

        case = CaseList.objects.filter(case_id=case_dict['case_id'])
        if case:
            try:
                case_version = case.values("case_version").first()["case_version"]
                case_dict["case_version"] = SetVersion.model_version(case_version)
                case.update_or_create(defaults=case_dict, case_id=case_dict['case_id'])
                return APIResponse(200, '用例修改成功')
            except Exception:
                return APIResponse(800005, '用例修改失败', success=False)
        else:
            return APIResponse(800004, '用例不存在', success=False)


class CaseDisableView(mixins.UpdateModelMixin, generics.GenericAPIView):
    authentication_classes = [CustomJsonToken]
    permission_classes = (IsAuthenticated,)

    queryset = CaseList.objects.all()
    serializer_class = CaseDisableSerializer

    @swagger_auto_schema(tags=["用例"],
                         operation_id="CaseDisable",
                         operation_summary='用例禁用启用',
                         operation_description='1:启用；2:禁用',
                         responses={800004: "用例不存在",
                                    800006: "操作失败，用例状态不正确",
                                    200: serializer_class})
    def put(self, request, *args, **kwargs):
        try:
            case_id = request.data.get('case_id')
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
            CaseList.objects.get(case_id=case_id)
        except CaseList.DoesNotExist:
            return APIResponse(800004, '用例不存在', success=False)

        try:
            CaseList.objects.filter(case_id=case_id).get(is_disable=is_disable)
            return APIResponse(800006, '操作失败，用例状态不正确', success=False)
        except CaseList.DoesNotExist:
            case = CaseList.objects.filter(case_id=case_id).first()
            if case:
                CaseList.objects.update_or_create(defaults={'is_disable': is_disable}, case_id=case_id)
                return APIResponse(200, '操作成功')
        return APIResponse(200, '操作成功')
