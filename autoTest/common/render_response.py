"""
自定义返回处理
"""
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response


class CustomerRenderer(JSONRenderer):
    # 重构render方法
    def render(self, data, accepted_media_type=None, renderer_context=None):
        res = {}
        if renderer_context:
            code = data.pop('code', renderer_context["response"].status_code)
            if isinstance(data, dict) and code == 200:
                res["message"] = data.pop('msg', '查询成功')
                res["code"] = data.pop('code', renderer_context["response"].status_code)
                res["success"] = True
                res["data"] = data

            else:
                res["message"] = data["message"]
                res["code"] = renderer_context["response"].status_code
                res["success"] = data["success"]
                res["data"] = data["data"]

            return super().render(res, accepted_media_type, renderer_context)
        else:
            return super().render(data, accepted_media_type, renderer_context)


class APIResponse(Response):
    def __init__(self, code=200, msg='请求成功', data=None, status=None, headers=None, success=True, **kwargs):
        dic = {'code': code, 'message': msg, 'success': success, 'data': None}
        if data:
            dic['data'] = data
        dic.update(kwargs)  # 可以灵活的添加，需要返回的键值对
        super().__init__(data=dic, status=status, headers=headers)
