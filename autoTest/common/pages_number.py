"""
自定义分页、重写数据返回
"""
from collections import OrderedDict
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class PageNumber(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'size'
    page_query_param = 'page'
    max_page_size = None

    # 重写方法，去掉next等字段，自定义返回
    def get_paginated_response(self, data):
        try:
            size = int(self.request.query_params["size"])
        except Exception:
            size = self.page_size

        return Response(OrderedDict([
                # 当前结果总条数
                ('total', self.page.paginator.count),
                # 当前结果总页数
                ('total_page', self.page.paginator.num_pages),
                # 当前传入的页数
                ('page', self.page.number),
                # 当前传入的每页显示条数
                ('size', size),
                ('list', data),
            ]))
