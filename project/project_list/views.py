from rest_framework import filters, mixins, generics
from rest_framework.generics import GenericAPIView
from django_filters import rest_framework
from autoTest.common.render_response import APIResponse
from rest_framework.permissions import IsAuthenticated
from autoTest.common.auth import CustomJsonToken
from project.project_list.models import ProjectList
from project.project_serializers import ProjectListSerializer
from project.project_filter import ProjectListFilter
from autoTest.common.search_time import SearchTime


# Create your views here.
class ProjectListView(mixins.ListModelMixin, generics.GenericAPIView):
    authentication_classes = [CustomJsonToken]
    permission_classes = (IsAuthenticated,)

    queryset = ProjectList.objects.filter(is_delete=False).all().order_by("-created_tm")
    serializer_class = ProjectListSerializer
    filter_class = ProjectListFilter
    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)

    def post(self, request, *args, **kwargs):
        """
        post: 项目列表信息

        时间段查询需要传时间戳
        """
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
            return APIResponse(40014, '参数错误', success=False)

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
            search_dict["editor"] = editor
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
