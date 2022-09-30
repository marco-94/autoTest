import jwt
from django.conf import settings
from rest_framework_jwt.authentication import BaseJSONWebTokenAuthentication
from rest_framework_jwt.authentication import get_authorization_header, jwt_decode_handler
from rest_framework.exceptions import AuthenticationFailed


class CustomJsonToken(BaseJSONWebTokenAuthentication):

    def authenticate(self, request):
        # 获取请求头里面的AUTHORIZATION参数的token值，或者我们自身规定客户端将自携带在哪里，再对应取即可
        jwt_value = get_authorization_header(request)

        if not jwt_value:
            raise AuthenticationFailed('Authorization 字段是必须的')

        try:
            # 通过解码token获取其在存储的用户信息，例如：ID、用户名、Email等等
            payload = jwt_decode_handler(jwt_value)
        except jwt.ExpiredSignature:
            raise AuthenticationFailed('签名过期')
        except jwt.DecodeError:
            raise AuthenticationFailed('解码错误')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('不合法的token')

        # 根据解码后得到的用户信息，再通过去对User表进行查询，得到user对象（在以下方法的源码内）
        user = self.authenticate_credentials(payload)

        return user, jwt_value
