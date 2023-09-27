"""
封装请求方法
"""
import requests
from autoTest.common.render_response import APIResponse


class RequestMethod:

    @staticmethod
    def get_method(url, headers=None, params=None, data=None):
        """封装get方法"""
        try:
            res = requests.get(url=url, headers=headers, params=params, data=data)
            return res
        except Exception as e:
            return APIResponse(400013, "get请求错误: %s" % e, success=False)

    @staticmethod
    def post_method_params(url, headers, params=None):
        """封装post方法"""
        try:
            res = requests.post(url=url, headers=headers, params=params)
            return res
        except Exception as e:
            return APIResponse(400013, "post请求错误: %s" % e, success=False)

    @staticmethod
    def post_method(url, headers=None, json=None, data=None):
        """封装post方法"""
        try:
            res = requests.post(url=url, headers=headers, json=json, data=data)
            return res
        except Exception as e:
            return APIResponse(400013, "post请求错误: %s" % e, success=False)

    @staticmethod
    def delete_method(url, headers, json=None):
        """封装delete方法"""
        try:
            res = requests.delete(url=url, headers=headers, json=json)
            return res
        except Exception as e:
            return APIResponse(400013, "delete请求错误: %s" % e, success=False)

    @staticmethod
    def put_method(url, headers, json=None):
        """封装put方法"""
        try:
            res = requests.put(url=url, headers=headers, json=json)
            return res
        except Exception as e:
            return APIResponse(400013, "put请求错误: %s" % e, success=False)
