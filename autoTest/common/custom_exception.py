"""
自定义异常处理
"""
from rest_framework.views import exception_handler
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.status import HTTP_200_OK
from autoTest.common.render_response import APIResponse


class MyException(APIException):
    status_code = HTTP_200_OK

    def __init__(self, detail):
        self.detail = detail


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        response.data.clear()
        response.data['message'] = '请求成功'
        response.data['code'] = response.status_code
        response.data['success'] = False
        response.data['data'] = None

        if response.status_code == 404:
            try:
                response.data['message'] = response.data.pop('detail')
                response.data['message'] = "Not found"
            except KeyError:
                response.data['message'] = "Not found"

        if response.status_code == 400:
            response.data['message'] = '参数输入不正确'

        elif response.status_code == 401:
            response.data['message'] = "身份验证失败"

        elif response.status_code >= 500:
            response.data['message'] = "服务器错误"

        elif response.status_code == 403:
            response.data['message'] = "无访问权限，请重新登录或稍后再试！"

        elif response.status_code == 405:
            response.data['message'] = '请求方法不正确'
    # else:
    #     return APIResponse(500, '服务器错误', status=status.HTTP_500_INTERNAL_SERVER_ERROR, success=False)
    return response
