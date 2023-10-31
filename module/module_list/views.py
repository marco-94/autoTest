from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, mixins, generics
from django_filters import rest_framework
from rest_framework.response import Response
from autoTest.common.render_response import APIResponse
from rest_framework.permissions import IsAuthenticated
from autoTest.common.auth import CustomJsonToken
from project.project_list.models import ProjectList
from module.module_list.models import ModuleList
from module.module_detail.models import ModuleDetail
from module.module_serializers import *
from module.module_filter import ModuleListFilter
from autoTest.common.search_time import SearchTime
from autoTest.common.render_response import CustomerRenderer
from autoTest.base.base_views import GetLoginUser
from rest_framework.viewsets import GenericViewSet
from rest_framework_jwt.settings import api_settings
from autoTest.common.set_version import SetVersion
from django.db.models import Q
from django.core import serializers

jwt_decode_handler = api_settings.JWT_DECODE_HANDLER


# Create your views here.
class ModuleListView(mixins.ListModelMixin, generics.GenericAPIView):
    authentication_classes = [CustomJsonToken]
    permission_classes = (IsAuthenticated,)
    renderer_classes = [CustomerRenderer]

    queryset = ModuleList.objects.all().order_by("-created_tm")
    serializer_class = ModuleListSerializer
    filter_class = ModuleListFilter
    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)

    @swagger_auto_schema(tags=['模块'],
                         operation_id="ModuleList",
                         operation_summary='模块列表',
                         operation_description='时间段查询需要传时间戳',
                         responses={"400014": "参数错误", 200: serializer_class})
    def post(self, request, *args, **kwargs):
        """模块列表信息 """
        try:
            module_id = request.data.get("module_id")
            project = request.data.get("project")
            module_name = request.data.get("module_name")
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

        if module_id:
            search_dict["module_id"] = module_id
        if module_name:
            search_dict["module_name__icontains"] = module_name
        if editor:
            search_dict["editor__icontains"] = editor
        if is_disable:
            search_dict["is_disable"] = 1
        if "is_disable" in search_dict and not is_disable:
            search_dict["is_disable"] = 0

        # 所属项目列表
        project_list = []

        if project:
            # 如果输入的字符串为整数（精确搜索）
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
            # 如果输入的字符串不为整数（精确搜索）
            else:
                try:
                    project_id = ProjectList.objects.filter(project_name__icontains=project).values('project_id')
                    for i in project_id:
                        project_list.append(int(i["project_id"]))
                except ProjectList.DoesNotExist:
                    return APIResponse(200, '查询成功', success=True)

        # 入参时间格式化
        if created_start_time and created_end_time:
            SearchTime().search_time_conversion(created_start_time, created_end_time, search_dict)
        print(project_list)
        # 由于覆盖了list方法，导致丢失了分页返回，故加上分页返回
        if not project_list:
            page_queryset = self.paginate_queryset(queryset=self.queryset.filter(**search_dict))
        else:
            page_queryset = self.paginate_queryset(
                queryset=self.queryset.filter(**search_dict, belong_project_id__in=project_list))
        # post请求加上分页条件查询
        if page_queryset is not None:
            serializer = self.get_serializer(page_queryset, many=True)
            return self.get_paginated_response(serializer.data)

        serializer_data = self.get_serializer(instance=page_queryset, many=True)

        return self.get_paginated_response(serializer_data.data)


class ModuleCreateViews(mixins.CreateModelMixin, GenericViewSet):
    authentication_classes = [CustomJsonToken]
    permission_classes = (IsAuthenticated,)

    queryset = ModuleList.objects.all()
    serializer_class = ModuleCreateSerializer
    filter_class = ModuleListFilter
    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)

    @swagger_auto_schema(tags=['模块'],
                         operation_id="ModuleCreate",
                         operation_summary='新增模块',
                         operation_description='模块名称必填且唯一',
                         responses={
                             400014: "参数错误",
                             400013: "请检查输入字段是否正确(必填字段、未定义字段)",
                             600001: "模块名称长度需要1到20位",
                             600002: "模块已存在",
                             600003: "模块创建失败",
                             200: "新增成功"
                         })
    def create(self, request, *args, **kwargs):
        """新增模块"""
        # 新增数据时，需要把入参同时存放到ModuleList和ModuleDetail表，故先把入参按照models定义，拆分成两个字典，非上述表字段，不处理
        module_dict = {}
        detail_dict = {}
        for item in request.data.items():
            if item[0] in [field.name for field in ModuleList._meta.get_fields()]:
                module_dict[item[0]] = item[1]
            elif item[0] in [field.name for field in ModuleDetail._meta.get_fields()]:
                detail_dict[item[0]] = item[1]

        # 获取当前登录用户信息
        user = GetLoginUser().get_login_user(request)
        if user["code"] == 200:
            module_dict["editor"] = user["username"]
        else:
            return Response(user)

        # 检查模块名称是否有填写
        if "module_name" not in list(module_dict.keys()):
            return APIResponse(400013, '请检查输入字段是否正确(必填字段、未定义字段)', success=False)
        else:
            if len(module_dict["module_name"]) > 20 or len(module_dict["module_name"]) < 1:
                return APIResponse(600001, '模块名称长度需要1到20位', success=False)

        if "belong_project" not in list(module_dict.keys()):
            return APIResponse(400013, '请检查输入字段是否正确(必填字段、未定义字段)', success=False)

        module_dict["belong_project_id"] = module_dict["belong_project"]
        del module_dict["belong_project"]
        try:
            ProjectList.objects.get(project_id=module_dict["belong_project_id"])
        except ProjectList.DoesNotExist:
            return APIResponse(500004, '项目不存在', success=False)

        module_name = str(module_dict["module_name"])
        try:
            ModuleList.objects.get(module_name=module_name)
            return APIResponse(600002, '模块已存在', success=False)
        except ModuleList.DoesNotExist:
            try:
                module_create = ModuleList.objects.create(**module_dict)
                if module_create:
                    module_id = ModuleList.objects.filter(module_name=module_name).values('module_id').first()
                    ModuleDetail.objects.update_or_create(defaults=detail_dict, module_info_id=module_id["module_id"])
                    return APIResponse(200, '模块创建成功')
            except Exception:
                return APIResponse(600003, '模块创建失败', success=False)
            

class ModuleEditViews(mixins.UpdateModelMixin, generics.GenericAPIView):
    authentication_classes = [CustomJsonToken]
    permission_classes = (IsAuthenticated,)

    queryset = ModuleList.objects.all()
    serializer_class = ModuleEditSerializer
    filter_class = ModuleListFilter
    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)

    @swagger_auto_schema(tags=['模块'],
                         operation_id="ModuleEdit",
                         operation_summary='模块编辑',
                         operation_description='模块名称唯一',
                         responses={
                             400014: "参数错误",
                             400013: "请检查输入字段是否正确(必填字段、未定义字段)",
                             600001: "模块名称长度需要1到20位",
                             600002: "模块名称已存在",
                             600004: "模块不存在",
                             600005: "模块修改失败",
                             200: serializer_class
                         })
    def put(self, request, *args, **kwargs):
        """编辑模块"""
        # 修改数据时，需要把入参同时存放到列表和详情两个表，故先把入参按照models定义，拆分成两个字典，非上述表字段，不处理
        module_dict = {}
        detail_dict = {}
        for item in request.data.items():
            if item[0] in [field.name for field in ModuleList._meta.get_fields()]:
                module_dict[item[0]] = item[1]
            elif item[0] in [field.name for field in ModuleDetail._meta.get_fields()]:
                detail_dict[item[0]] = item[1]

        # 获取当前登录用户信息
        user = GetLoginUser().get_login_user(request)
        if user["code"] == 200:
            module_dict["editor"] = user["username"]
        else:
            return Response(user)

        # 检查模块名称是否有填写
        if "module_name" not in list(module_dict.keys()):
            return APIResponse(400013, '请检查输入字段是否正确(必填字段、未定义字段)', success=False)
        else:
            if len(module_dict["module_name"]) > 20 or len(module_dict["module_name"]) < 1:
                return APIResponse(600001, '模块名称长度需要1到20位', success=False)

        # 非当前修改数据条件下，判断名称是否存在
        if ModuleList.objects.filter(module_name=module_dict["module_name"]).count() > 0:
            module_info = ModuleList.objects.filter(module_name=module_dict["module_name"]).values('module_id')
            # 查询到的同名数据ID与当前修改数据ID不一致时，不允许修改
            if not str(module_info[0]["module_id"]) == str(module_dict['module_id']):
                return APIResponse(600002, '模块名称已存在', success=False)

        module = ModuleList.objects.filter(module_id=module_dict['module_id'])
        if module:
            try:
                module_version = module.values("module_version").first()["module_version"]
                module_dict["module_version"] = SetVersion.model_version(module_version)
                module_update = module.update_or_create(defaults=module_dict, module_id=module_dict['module_id'])
                if module_update:
                    ModuleDetail.objects.update_or_create(defaults=detail_dict, module_info_id=module_dict['module_id'])
                    return APIResponse(200, '模块修改成功')
            except Exception:
                return APIResponse(600005, '模块修改失败', success=False)
        else:
            return APIResponse(600005, '模块不存在', success=False)


class ModuleDisableView(mixins.UpdateModelMixin, generics.GenericAPIView):
    authentication_classes = [CustomJsonToken]
    permission_classes = (IsAuthenticated,)

    queryset = ModuleList.objects.all()
    serializer_class = ModuleDisableSerializer

    @swagger_auto_schema(tags=["模块"],
                         operation_id="ModuleDisable",
                         operation_summary='模块禁用启用',
                         operation_description='1:启用；2:禁用',
                         responses={600005: "模块不存在",
                                    600006: "操作失败，模块状态不正确",
                                    200: serializer_class})
    def put(self, request, *args, **kwargs):
        try:
            module_id = request.data.get('module_id')
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
            ModuleList.objects.get(module_id=module_id)
        except ModuleList.DoesNotExist:
            return APIResponse(600004, '模块不存在', success=False)

        try:
            ModuleList.objects.filter(module_id=module_id).get(is_disable=is_disable)
            return APIResponse(600006, '操作失败，模块状态不正确', success=False)
        except ModuleList.DoesNotExist:
            module = ModuleList.objects.filter(module_id=module_id).first()
            if module:
                ModuleList.objects.update_or_create(defaults={'is_disable': is_disable}, module_id=module_id)
                return APIResponse(200, '操作成功')
        return APIResponse(200, '操作成功')
