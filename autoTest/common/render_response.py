"""
自定义返回处理
"""
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response


class CustomerRenderer(JSONRenderer):
    # 重构render方法
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if renderer_context:
            if isinstance(data, dict):
                msg = data.pop('msg', '查询成功')
                code = data.pop('code', renderer_context["response"].status_code)
            else:
                msg = '查询成功'
                code = renderer_context["response"].status_code

            ret = {
                'message': msg,
                'code': code,
                'success': True,
                'data': data,
            }
            # 返回JSON数据
            return super().render(ret, accepted_media_type, renderer_context)
        else:
            return super().render(data, accepted_media_type, renderer_context)


class APIResponse(Response):
    def __init__(self, code=100, msg='查询成功', data=None, status=None, headers=None, success=True, **kwargs):
        dic = {'code': code, 'message': msg, 'success': success, 'data': []}
        if data:
            dic['data'] = data
        dic.update(kwargs)  # 可以灵活的添加，需要返回的键值对
        super().__init__(data=dic, status=status, headers=headers)