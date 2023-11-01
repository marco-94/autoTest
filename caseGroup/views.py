from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, mixins, generics
from django_filters import rest_framework
from rest_framework.response import Response
from autoTest.common.render_response import APIResponse
from rest_framework.permissions import IsAuthenticated
from autoTest.common.auth import CustomJsonToken
from module.module_list.models import ModuleList
from caseGroup.models import CaseGroupList
from caseGroup.case_group_serializers import *
from caseGroup.case_group_filter import *
from autoTest.common.search_time import SearchTime
from autoTest.common.render_response import CustomerRenderer
from autoTest.base.base_views import GetLoginUser
from rest_framework.viewsets import GenericViewSet
from rest_framework_jwt.settings import api_settings
from autoTest.common.set_version import SetVersion
from autoTest.common.global_configuration import global_id

jwt_decode_handler = api_settings.JWT_DECODE_HANDLER


# Create your views here.
class CaseGroupListView(mixins.ListModelMixin, generics.GenericAPIView):
    authentication_classes = [CustomJsonToken]
    permission_classes = (IsAuthenticated,)
    renderer_classes = [CustomerRenderer]

    queryset = CaseGroupList.objects.all().order_by("-created_tm")
    serializer_class = CaseGroupListSerializer
    filter_class = CaseGroupListFilter
    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)

    @swagger_auto_schema(tags=['用例组'],
                         operation_id="CaseGroupList",
                         operation_summary='用例组列表',
                         operation_description='时间段查询需要传时间戳',
                         responses={"400014": "参数错误", 200: serializer_class})
    def post(self, request, *args, **kwargs):
        """用例组列表信息 """
        try:
            case_group_id = request.data.get("case_group_id")
            module = request.data.get("module")
            project = request.data.get("project")
            case_group_name = request.data.get("case_group_name")
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

        if case_group_id:
            search_dict["case_group_id"] = case_group_id
        if case_group_name:
            search_dict["case_group_name__icontains"] = case_group_name
        if editor:
            search_dict["editor__icontains"] = editor
        if is_disable:
            search_dict["is_disable"] = 1
        if "is_disable" in search_dict and not is_disable:
            search_dict["is_disable"] = 0

        # 所属项目查询
        project_list = []

        # 所属项目搜索：项目ID为精确搜索，项目名称为模糊搜索
        if project:
            # 如果输入的字符串为整数
            if project.isdigit():
                try:
                    ProjectList.objects.get(project_id__exact=int(project))
                    project_list.append(int(project))
                except ProjectList.DoesNotExist:
                    try:
                        project_id = ProjectList.objects.filter(project_name__icontains=project).values('project_id')
                        if project_id:
                            for i in project_id:
                                project_list.append(int(i["project_id"]))
                        else:
                            return APIResponse(200, '查询成功', success=True)
                    except ProjectList.DoesNotExist:
                        return APIResponse(200, '查询成功', success=True)
            # 如果输入的字符串不为整数
            else:
                try:
                    project_id = ProjectList.objects.filter(project_name__icontains=project).values('project_id')
                    for i in project_id:
                        project_list.append(int(i["project_id"]))
                except ProjectList.DoesNotExist:
                    return APIResponse(200, '查询成功', success=True)

        # 所属模块查询
        module_list = []

        # 所属模块搜索：模块ID为精确搜索，模块名称为模糊搜索
        if module:
            # 如果输入的字符串为整数
            if module.isdigit():
                try:
                    ModuleList.objects.get(module_id__exact=int(module))
                    module_list.append(int(module))
                except ModuleList.DoesNotExist:
                    try:
                        module_id = ModuleList.objects.filter(module_name__icontains=module).values('module_id')
                        if module_id:
                            for i in module_id:
                                module_list.append(int(i["module_id"]))
                        else:
                            return APIResponse(200, '查询成功', success=True)
                    except ModuleList.DoesNotExist:
                        return APIResponse(200, '查询成功', success=True)
            # 如果输入的字符串不为整数
            else:
                try:
                    module_id = ModuleList.objects.filter(module_name__icontains=module).values('module_id')
                    for i in module_id:
                        module_list.append(int(i["module_id"]))
                except ModuleList.DoesNotExist:
                    return APIResponse(200, '查询成功', success=True)

        # 入参时间格式化
        if created_start_time and created_end_time:
            SearchTime().search_time_conversion(created_start_time, created_end_time, search_dict)

        # 由于覆盖了list方法，导致丢失了分页返回，故加上分页返回
        page_queryset = self.paginate_queryset(queryset=self.queryset.filter(**search_dict))

        # 仅筛选所属模块
        if module_list:
            page_queryset = self.paginate_queryset(queryset=self.queryset.filter(**search_dict,
                                                                                 module_id__in=module_list))
        # 仅筛选所属项目
        if project_list:
            page_queryset = self.paginate_queryset(queryset=self.queryset.filter(**search_dict,
                                                                                 project_id__in=project_list))
        # 同时筛选所属模块和项目
        if module_list and project_list:
            page_queryset = self.paginate_queryset(queryset=self.queryset.filter(**search_dict,
                                                                                 project_id__in=project_list,
                                                                                 module_id__in=module_list))

        # post请求加上分页条件查询
        serializer = self.get_serializer(instance=page_queryset, many=True)

        if page_queryset is not None:
            serializer = self.get_serializer(page_queryset, many=True)

        return self.get_paginated_response(serializer.data)


class CaseGroupCreateViews(mixins.CreateModelMixin, GenericViewSet):
    authentication_classes = [CustomJsonToken]
    permission_classes = (IsAuthenticated,)

    queryset = CaseGroupList.objects.all()
    serializer_class = CaseGroupCreateSerializer
    filter_class = CaseGroupListFilter
    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)

    @swagger_auto_schema(tags=['用例组'],
                         operation_id="CaseGroupCreate",
                         operation_summary='新增用例组',
                         operation_description='用例组名称必填且唯一',
                         responses={
                             400014: "参数错误",
                             400013: "请检查输入字段是否正确(必填字段、未定义字段)",
                             700001: "用例组名称长度需要1到20位",
                             700002: "用例组已存在",
                             700003: "用例组创建失败",
                             200: "新增成功"
                         })
    def create(self, request, *args, **kwargs):
        """新增用例组"""
        # 新增数据时，筛选掉无用的入参
        case_group_dict = {}
        for item in request.data.items():
            if item[0] in [field.name for field in CaseGroupList._meta.get_fields()]:
                case_group_dict[item[0]] = item[1]

        # 获取当前登录用户信息
        user = GetLoginUser().get_login_user(request)
        if user["code"] == 200:
            case_group_dict["editor"] = user["username"]
        else:
            return Response(user)

        # 检查用例组名称是否有填写
        if "case_group_name" not in list(case_group_dict.keys()):
            return APIResponse(400013, '请检查输入字段是否正确(必填字段、未定义字段)', success=False)
        else:
            if len(case_group_dict["case_group_name"]) > 20 or len(case_group_dict["case_group_name"]) < 1:
                return APIResponse(700001, '用例组名称长度需要1到20位', success=False)

        if "module" not in list(case_group_dict.keys()):
            return APIResponse(400013, '请检查输入字段是否正确(必填字段、未定义字段)', success=False)

        case_group_dict["module_id"] = case_group_dict.pop("module")

        try:
            ModuleList.objects.get(module_id=case_group_dict["module_id"])
            # 通过传入的模块ID，在模块列表找到对应的项目ID
            module = ModuleList.objects.filter(module_id=case_group_dict["module_id"])
            project_id = module.values("belong_project_id").first()["belong_project_id"]
            case_group_dict["project_id"] = project_id
        except ModuleList.DoesNotExist:
            return APIResponse(600004, '模块不存在', success=False)

        try:
            CaseGroupList.objects.get(case_group_name=case_group_dict["case_group_name"])
            return APIResponse(700002, '用例组已存在', success=False)
        except CaseGroupList.DoesNotExist:
            print(case_group_dict)
            try:
                CaseGroupList.objects.create(**case_group_dict)
                return APIResponse(200, '用例组创建成功')
            except Exception:
                return APIResponse(700003, '用例组创建失败', success=False)


class CaseGroupEditViews(mixins.UpdateModelMixin, generics.GenericAPIView):
    authentication_classes = [CustomJsonToken]
    permission_classes = (IsAuthenticated,)

    queryset = CaseGroupList.objects.all()
    serializer_class = CaseGroupEditSerializer
    filter_class = CaseGroupListFilter
    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)

    @swagger_auto_schema(tags=['用例组'],
                         operation_id="CaseGroupEdit",
                         operation_summary='用例组编辑',
                         operation_description='用例组名称唯一',
                         responses={
                             400014: "参数错误",
                             400013: "请检查输入字段是否正确(必填字段、未定义字段)",
                             700001: "用例组名称长度需要1到20位",
                             700002: "用例组名称已存在",
                             700004: "用例组不存在",
                             700005: "用例组修改失败",
                             200: serializer_class
                         })
    def put(self, request, *args, **kwargs):
        """编辑用例组"""
        # 修改数据时，需要把入参同时存放到列表和详情两个表，故先把入参按照models定义，拆分成两个字典，非上述表字段，不处理
        case_group_dict = {}
        for item in request.data.items():
            if item[0] in [field.name for field in CaseGroupList._meta.get_fields()]:
                case_group_dict[item[0]] = item[1]

        # 获取当前登录用户信息
        user = GetLoginUser().get_login_user(request)
        if user["code"] == 200:
            case_group_dict["editor"] = user["username"]
        else:
            return Response(user)

        # 检查用例组名称是否有填写
        if "case_group_name" not in list(case_group_dict.keys()):
            return APIResponse(400013, '请检查输入字段是否正确(必填字段、未定义字段)', success=False)
        else:
            if len(case_group_dict["case_group_name"]) > 20 or len(case_group_dict["case_group_name"]) < 1:
                return APIResponse(700001, '用例组名称长度需要1到20位', success=False)

        # 非当前修改数据条件下，判断名称是否存在
        if CaseGroupList.objects.filter(case_group_name=case_group_dict["case_group_name"]).count() > 0:
            case_group_info = CaseGroupList.objects.filter(case_group_name=case_group_dict["case_group_name"]).values(
                'case_group_id')
            # 查询到的同名数据ID与当前修改数据ID不一致时，不允许修改
            if not str(case_group_info[0]["case_group_id"]) == str(case_group_dict['case_group_id']):
                return APIResponse(700002, '用例组名称已存在', success=False)

        case_group = CaseGroupList.objects.filter(case_group_id=case_group_dict['case_group_id'])
        if case_group:
            try:
                case_group_version = case_group.values("case_group_version").first()["case_group_version"]
                case_group_dict["case_group_version"] = SetVersion.model_version(case_group_version)
                case_group.update_or_create(defaults=case_group_dict, case_group_id=case_group_dict['case_group_id'])
                return APIResponse(200, '用例组修改成功')
            except Exception:
                return APIResponse(700005, '用例组修改失败', success=False)
        else:
            return APIResponse(700004, '用例组不存在', success=False)


class CaseGroupDisableView(mixins.UpdateModelMixin, generics.GenericAPIView):
    authentication_classes = [CustomJsonToken]
    permission_classes = (IsAuthenticated,)

    queryset = CaseGroupList.objects.all()
    serializer_class = CaseGroupDisableSerializer

    @swagger_auto_schema(tags=["用例组"],
                         operation_id="CaseGroupDisable",
                         operation_summary='用例组禁用启用',
                         operation_description='1:启用；2:禁用',
                         responses={700004: "用例组不存在",
                                    700006: "操作失败，用例组状态不正确",
                                    200: serializer_class})
    def put(self, request, *args, **kwargs):
        try:
            case_group_id = request.data.get('case_group_id')
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
            CaseGroupList.objects.get(case_group_id=case_group_id)
        except CaseGroupList.DoesNotExist:
            return APIResponse(700004, '用例组不存在', success=False)

        try:
            CaseGroupList.objects.filter(case_group_id=case_group_id).get(is_disable=is_disable)
            return APIResponse(700006, '操作失败，用例组状态不正确', success=False)
        except CaseGroupList.DoesNotExist:
            case_group = CaseGroupList.objects.filter(case_group_id=case_group_id).first()
            if case_group:
                CaseGroupList.objects.update_or_create(defaults={'is_disable': is_disable}, case_group_id=case_group_id)
                return APIResponse(200, '操作成功')
        return APIResponse(200, '操作成功')
