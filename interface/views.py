from drf_yasg.utils import swagger_auto_schema, param_list_to_odict
from drf_yasg import openapi
from rest_framework import filters, mixins, generics
from django_filters import rest_framework
from rest_framework.response import Response
from autoTest.common.render_response import APIResponse
from rest_framework.permissions import IsAuthenticated
from autoTest.common.auth import CustomJsonToken
from autoTest.common.search_time import SearchTime
from autoTest.common.render_response import CustomerRenderer
from autoTest.common.password_encryption import PasswordEncryption
from autoTest.common.requset_method import RequestMethod
from rest_framework.viewsets import GenericViewSet
from rest_framework_jwt.settings import api_settings
from rest_framework.parsers import MultiPartParser, FileUploadParser
from autoTest.base.base_views import GetLoginUser
from interface.models import *
from interface.interface_serializers import *
import requests
import ast
import json
import chardet
from retrying import retry
from rest_framework import status
from autoTest.common.utils import interface_assert_equal, get_domain
from rest_framework.viewsets import ModelViewSet
from django.core.files.uploadedfile import InMemoryUploadedFile
from autoTest.common.global_configuration import global_id


# Create your views here.
class ErpLoginView(mixins.ListModelMixin, generics.GenericAPIView):
    authentication_classes = []
    permission_classes = ()
    queryset = ErpLogin.objects.all()
    serializer_class = ErpLoginSerializer

    @swagger_auto_schema(tags=['接口'],
                         operation_id="ErpLogin",
                         operation_summary='ERP用户登录',
                         operation_description='使用erp的账号密码进行登录</br> 测试环境：1，正式环境：2',
                         responses={
                             400014: "参数错误",
                             400013: "请检查输入字段是否正确(必填字段、未定义字段)",
                             200: "登录成功"
                         })
    def post(self, request, *args, **kwargs):
        result_json = {"success": True, "token": "", "msg": "登录成功", "code": 200}
        result = None
        try:
            username = request.data.get("username")
            password = request.data.get("password")
            environment = request.data.get("environment")
        except Exception:
            return APIResponse(400014, '参数错误', success=False)

        erp_login_dict = {}
        for item in request.data.items():
            if item[0] in [field.name for field in ErpLogin._meta.get_fields()]:
                erp_login_dict[item[0]] = item[1]

        # 检查必填字段是否有填写
        if "username" not in list(erp_login_dict.keys()) or "password" not in list(
                erp_login_dict.keys()) or "environment" not in list(erp_login_dict.keys()):
            return APIResponse(400013, '请检查输入字段是否正确(必填字段、未定义字段)', success=False)

        if environment not in (1, 2):
            return APIResponse(400014, '参数错误', success=False)

        domain = get_domain(environment)["environment"]

        # 密码加密
        public_keys = PasswordEncryption().get_public_key(domain)
        passwords = PasswordEncryption().encrpt(password, public_keys)

        # 登录流程
        try:
            headers = {"Content-Type": "application/json"}
            authorize_params = {
                "scope": "openid",
                "response_type": "code",
                "client_id": "585014642717982720",
                "redirect_url": "https://localhost:8443/uac/",
                "state": "e268443e43d93dab7ebef303bbe9642f",
                "auth_type": "BPassword"
            }
            authorize_response = RequestMethod.get_method(url=domain + "/api/sso/oidc/authorize/",
                                                          params=authorize_params)
            result = interface_assert_equal(authorize_response)

            execute_json = {
                "c_name": "BPasswordLogin",
                "input_param": {
                    "regionCode": "86",
                    "username": username,
                    "password": passwords
                },
                "code_key": authorize_response.json()['data']['code_key']
            }

            execute_response = RequestMethod.post_method(json=execute_json)
            result = interface_assert_equal(execute_response)

            access_json = {
                "client_id": 585014642717982720,
                "client_secret": "b9c7398eebe909a01603d5fba2c55086",
                "code": execute_response.json()['data']['code'],
                "state": execute_response.json()['data']['state'],
                "userId": execute_response.json()['data']['userId']
            }
            access_token_response = RequestMethod.post_method(json=access_json)
            result = interface_assert_equal(access_token_response)

            result_json["token"] = access_token_response.json()['data']['access_token']
        finally:
            if not result["success"]:
                result_json["code"] = result["code"]
                result_json["msg"] = result["msg"]
                result_json["success"] = result["success"]
            if result["success"]:
                detail_dict = {"username": username,
                               "environment": environment,
                               "token": result_json["token"]
                               }
                ErpLogin.objects.update_or_create(defaults=detail_dict, username=username, environment=environment)
            return APIResponse(result_json["code"],
                               result_json["msg"],
                               {"token": result_json["token"]},
                               success=result_json["success"])


class InterfaceQuickTestView(mixins.ListModelMixin, generics.GenericAPIView):
    authentication_classes = []
    permission_classes = ()
    queryset = ApiInfo.objects.all()
    serializer_class = InterfaceQuickTestSerializer

    @swagger_auto_schema(tags=['接口'],
                         operation_id="InterfaceQuickTest",
                         operation_summary='接口快速测试',
                         operation_description='token和username，两者必须传一</br>' +
                                               '请求方式：1：get；2：post；3：put；4：delete</br>' +
                                               '请求参数格式：1：表单(form-data)；2：源数据(raw)；3：Restful</br>' +
                                               'headers、params、data传参格式均为字典格式</br>',
                         responses={
                             400014: "参数错误",
                             400013: "请检查输入字段是否正确(必填字段、未定义字段)",
                             200: "查询成功"
                         })
    def post(self, request, *args, **kwargs):
        try:
            request_type = request.data.get("request_type")
            api_address = request.data.get("api_address")
            request_parameter_type = request.data.get("request_parameter_type")
            headers = request.data.get("headers")
            params = request.data.get("params")
            data = request.data.get("data")
        except Exception:
            return APIResponse(400014, '参数错误', success=False)

        # 检查必填字段
        try:
            if not request_type or not api_address or not request_parameter_type:
                return APIResponse(400013, '请检查输入字段是否正确(必填字段、未定义字段)', success=False)
        except KeyError:
            return APIResponse(400013, '请检查输入字段是否正确(必填字段、未定义字段)', success=False)

        if request_type not in range(1, 5) or request_parameter_type not in range(1, 4):
            return APIResponse(400014, '参数错误', success=False)

        # 判断是否传入token和username，两者必须传一，如果token未传，则判断是否有登录保存信息
        # if not token:
        #     if not username:
        #         return APIResponse(400014, '参数错误', success=False)
        #     else:
        #         try:
        #             ErpLogin.objects.get(username=username, environment=environment)
        #         except Exception:
        #             return APIResponse(900001, '用户未登录或token已过期，请重新登录', success=False)
        #
        #         token = ErpLogin.objects.filter(username=username, environment=environment).values("token").first()
        #         if not token["token"]:
        #             return APIResponse(900001, '用户未登录或token已过期，请重新登录', success=False)

        # get请求方式
        if request_type == 1:
            response = RequestMethod.get_method(url=api_address, headers=headers, params=params)
            return Response(response.json())

        # post请求方式
        if request_type == 2:
            if request_parameter_type == 1:
                response = RequestMethod.post_method_params(url=api_address, headers=headers, params=params)
                return Response(response.json())
            if request_parameter_type == 2:
                if not data:
                    return APIResponse(400013, '请检查输入字段是否正确(必填字段、未定义字段)', success=False)
                response = RequestMethod().post_method(url=api_address, headers=headers, data=data)
                return Response(response.json())

        # put请求方式
        if request_type == 3:
            if not data:
                return APIResponse(400013, '请检查输入字段是否正确(必填字段、未定义字段)', success=False)
            response = RequestMethod().put_method(url=api_address, headers=headers, data=data)
            return Response(response.json())

        # delete请求方式
        if request_type == 4:
            if not data:
                return APIResponse(400013, '请检查输入字段是否正确(必填字段、未定义字段)', success=False)
            response = RequestMethod().delete_method(url=api_address, headers=headers, data=data)
            return Response(response.json())


class OssUploadsView(mixins.CreateModelMixin, generics.GenericAPIView):
    parser_classes = (MultiPartParser, FileUploadParser,)
    authentication_classes = [CustomJsonToken]
    permission_classes = (IsAuthenticated,)
    queryset = OssFile.objects.all()
    serializer_class = OssFileSerializer

    @swagger_auto_schema(tags=['接口'],
                         operation_id="OssUploads",
                         operation_summary='文件上传',
                         operation_description='',
                         responses={200: "上传成功"})
    def post(self, request, *args, **kwargs):
        """文件上传"""
        data = request.data

        # 获取当前登录用户信息
        user = GetLoginUser().get_login_user(request)
        if user["code"] == 200:
            data["editor"] = user["username"]
        else:
            return Response(user)

        data["file_id"] = global_id()["work_id"]

        upload_object = request.FILES.get("file")
        data["file_name"] = upload_object.name.split('.')[0]
        data["file_type"] = upload_object.content_type
        data["file_size"] = upload_object.size

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return APIResponse(200, '上传成功', success=True, data=serializer.data)
