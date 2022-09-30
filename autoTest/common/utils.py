"""
自定义jwt认证成功返回数据
:token  返回的jwt
:user   当前登录的用户信息[对象]
:request 当前本次客户端提交过来的数据
:role 角色
"""


def jwt_response_payload_handler(token, user=None, request=None, role=None):
    if user.first_name:
        name = user.first_name
    else:
        name = user.username
    return {
        'id': user.id,
        'name': name,
        'username': user.username,
        'token': token,
    }
    # return {
    #     'code': 100,
    #     'msg': '登录成功',
    #     'id': user.id,
    #     'username': user.username,
    #     'token': token
    # }
