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
from report.report_list.models import *
from report.report_serializers import *
from report.report_filter import *
from autoTest.common.search_time import SearchTime
from autoTest.common.render_response import CustomerRenderer
from autoTest.base.base_views import GetLoginUser
from rest_framework.viewsets import GenericViewSet
from rest_framework_jwt.settings import api_settings
from autoTest.common.set_version import SetVersion
from autoTest.common.global_configuration import global_id

jwt_decode_handler = api_settings.JWT_DECODE_HANDLER


class ReportCreateViews(mixins.CreateModelMixin, GenericViewSet):
    authentication_classes = [CustomJsonToken]
    permission_classes = (IsAuthenticated,)

    queryset = ReportList.objects.all()
    serializer_class = ReportListSerializer
    filter_class = ReportListFilter
    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)

    @swagger_auto_schema(tags=['报告'],
                         operation_id="ReportCreate",
                         operation_summary='新增报告',
                         operation_description='报告名称必填且唯一，所属用例和所属用例组只能存在其中一个',
                         responses={
                             400014: "参数错误",
                             600004: "项目不存在",
                             400013: "请检查输入字段是否正确(必填字段、未定义字段)",
                             900001: "报告名称长度需要1到20位",
                             900002: "报告已存在",
                             900003: "报告创建失败",
                             700004: "用例组不存在或已被禁用",
                             800004: "用例不存在或已被禁用",
                             200: "新增成功"
                         })
    def create(self, request, *args, **kwargs):
        """新增用例"""
        # 新增数据时，筛选掉无用的入参

        report_dict = {}
        for item in request.data.items():
            if item[0] in [field.name for field in ReportList._meta.get_fields()]:
                report_dict[item[0]] = item[1]

        # 检查用例名称和所属项目组是否有填写
        if "report_name" not in list(report_dict.keys()) or "editor" not in list(report_dict.keys()):
            return APIResponse(400013, '请检查输入字段是否正确(必填字段、未定义字段)', success=False)
        else:
            if len(report_dict["report_name"]) > 20 or len(report_dict["report_name"]) < 1:
                return APIResponse(900001, '报告名称长度需要1到20位', success=False)

        # 用例和用例组需要存在其中一个
        if "group" not in list(report_dict.keys()) and "case" not in list(report_dict.keys()):
            return APIResponse(400013, '请检查输入字段是否正确(必填字段、未定义字段)2', success=False)

        # 用例和用例组只能存在其中一个
        if "group" in list(report_dict.keys()) and "case" in list(report_dict.keys()):
            return APIResponse(400013, '请检查输入字段是否正确(必填字段、未定义字段)3', success=False)

        # 检查用例组是否存在
        if "group" in report_dict:
            # 变更字段名
            report_dict["group_id"] = report_dict.pop("group")
            try:
                CaseGroupList.objects.get(case_group_id=report_dict["group_id"], is_disable=False, is_delete=False)
            except Exception:
                return APIResponse(700004, '用例组不存在或已被禁用', success=False)

        # 检查用例是否存在
        if "case" in report_dict:
            report_dict["case_id"] = report_dict.pop("case")
            try:
                CaseList.objects.get(case_id=report_dict["case_id"], is_disable=False, is_delete=False)
            except Exception:
                return APIResponse(800004, '用例不存在或已被禁用', success=False)

        try:
            ReportList.objects.get(report_name=report_dict["report_name"])
            return APIResponse(900002, '报告已存在', success=False)
        except ReportList.DoesNotExist:
            try:
                report_dict["report_id"] = global_id()["work_id"]
                ReportList.objects.create(**report_dict)
                return APIResponse(200, '报告创建成功')
            except Exception:
                return APIResponse(900003, '报告创建失败', success=False)


class ReportListView(mixins.ListModelMixin, generics.GenericAPIView):
    authentication_classes = [CustomJsonToken]
    permission_classes = (IsAuthenticated,)
    renderer_classes = [CustomerRenderer]

    queryset = ReportList.objects.all().order_by("-created_tm")
    serializer_class = ReportListSerializer
    filter_class = ReportListFilter
    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)

    @swagger_auto_schema(tags=['报告'],
                         operation_id="ReportList",
                         operation_summary='报告列表',
                         operation_description='时间段查询需要传时间戳',
                         responses={"400014": "参数错误", 200: serializer_class})
    def post(self, request, *args, **kwargs):
        """报告列表信息 """

        try:
            report_id = request.data.get("report_id")
            case_id = request.data.get("case_id")
            group_id = request.data.get("group_id")
            report_name = request.data.get("report_name")
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

        if report_id:
            search_dict["report_id"] = report_id
        if case_id:
            search_dict["case_id"] = case_id
        if group_id:
            search_dict["group_id"] = group_id
        if report_name:
            search_dict["report_name__icontains"] = report_name
        if editor:
            search_dict["editor__icontains"] = editor

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
