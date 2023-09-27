"""
自定义jwt认证成功返回数据
:token  返回的jwt
:user   当前登录的用户信息[对象]
:request 当前本次客户端提交过来的数据
:role 角色
"""


def jwt_response_payload_handler(token, user=None):
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


def interface_assert_equal(response):
    """
            接口请求检查
            :param response:
            :return:
            """
    return_json = {"success": True, "msg": "", "code": 200}
    if response.status_code != 200 or response.json()['code'] != "200":
        return_json["success"] = False
        return_json["code"] = response.status_code
        try:
            if response.json()["code"] == '4010011002':
                update_yaml.UpdateYaml.up_yml("authorization", "")
            return_json["msg"] = str(response.json()['msg'])
        except Exception:
            return_json["msg"] = "接口错误：" + str(response.status_code)
    return return_json


def get_domain(environment):
    if environment == 1:
        environment = "https://erp-beta.yjzf.com"
    if environment == 2:
        environment = "https://erp.yjzf.com"
    return {"environment": environment}
