from user.user_list.models import Account
from jwt import ExpiredSignatureError
from autoTest.common.render_response import APIResponse
from rest_framework_jwt.settings import api_settings

# token解密
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER


class GetLoginUser:
    @staticmethod
    def get_login_user(request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION')
        except Exception:
            return APIResponse(400014, '参数错误', success=False)

        if token:
            try:
                # 解密token，提取user_id
                user_id = jwt_decode_handler(token)["user_id"]
                username = Account.objects.filter(user_id=user_id).values('username').first()
                return {"user_id": user_id, "username": username["username"], "code": 200}
            except ExpiredSignatureError:
                return APIResponse(4031, 'token已过期', success=False)
        else:
            return APIResponse(403, '无访问权限，请重新登录或稍后再试！', success=False)
