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


class CaseGroupCreateViews(mixins.CreateModelMixin, GenericViewSet):
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
                             200: "新增成功"
                         })
    def create(self, request, *args, **kwargs):
        """新增用例"""
        # 新增数据时，筛选掉无用的入参
        case_dict = {}
        for item in request.data.items():
            if item[0] in [field.name for field in CaseGroupList._meta.get_fields()]:
                case_dict[item[0]] = item[1]

        # 获取当前登录用户信息
        user = GetLoginUser().get_login_user(request)
        if user["code"] == 200:
            case_dict["editor"] = user["username"]
        else:
            return Response(user)

        # 检查用例名称是否有填写
        if "case_name" not in list(case_dict.keys()):
            return APIResponse(400013, '请检查输入字段是否正确(必填字段、未定义字段)', success=False)
        else:
            if len(case_dict["case_name"]) > 20 or len(case_dict["case_name"]) < 1:
                return APIResponse(800001, '用例名称长度需要1到20位', success=False)

        if "case_group" not in list(case_dict.keys()) or "module" not in list(
                case_dict.keys()) or "project" not in list(case_dict.keys()):
            return APIResponse(400013, '请检查输入字段是否正确(必填字段、未定义字段)', success=False)

        case_dict["case_group_id"] = case_dict.pop("case_group")
        case_dict["module_id"] = case_dict.pop("module")
        case_dict["project_id"] = case_dict.pop("project")

        try:
            # 判断用例组与模块
            case_group = CaseList.objects.filter(case_group_id=case_dict["case_group_id"])
            module_id = case_group.values("module_id").first()["module_id"]
            if not case_dict["module_id"] == module_id:
                return APIResponse(800008, '用例组与模块不匹配', success=False)
            
            # 判断模块与项目
            module = ModuleList.objects.filter(module_id=case_dict["module_id"])
            project_id = module.values("belong_project_id").first()["belong_project_id"]
            if not case_dict["project_id"] == project_id:
                return APIResponse(800007, '项目与模块不匹配', success=False)
        except ModuleList.DoesNotExist:
            return APIResponse(600004, '项目不存在', success=False)

        try:
            CaseGroupList.objects.get(case_name=case_dict["case_name"])
            return APIResponse(800002, '用例已存在', success=False)
        except CaseGroupList.DoesNotExist:
            try:
                CaseGroupList.objects.create(**case_dict)
                return APIResponse(200, '用例创建成功')
            except Exception:
                return APIResponse(800003, '用例创建失败', success=False)
