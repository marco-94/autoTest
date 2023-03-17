from drf_yasg.openapi import Schema
from drf_yasg.utils import swagger_auto_schema
import hashlib
from rest_framework import filters, mixins, generics
from rest_framework.generics import GenericAPIView
from django_filters import rest_framework
from rest_framework.viewsets import GenericViewSet
from user.user_list.models import Account, UserRole
from user.user_detail.models import UserDetail
from user import user_filter, user_serializers
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import viewsets
from rest_framework_jwt.settings import api_settings
from autoTest.common.auth import CustomJsonToken
from autoTest.common.render_response import APIResponse
from user.user_serializers import PasswordSerializer
from autoTest.common.search_time import SearchTime
from autoTest.common.render_response import CustomerRenderer

# jwt-token签发和校验配置
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


# Create your views here.
class UserCreateView(mixins.CreateModelMixin, GenericViewSet):
    authentication_classes = [CustomJsonToken]
    permission_classes = ()
    queryset = Account.objects.filter(is_delete=0).all()
    serializer_class = user_serializers.UserCreateSerializer
    filter_class = user_filter.UserFilter
    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    ordering = ['-created_tm']

    @swagger_auto_schema(tags=["用户"],
                         operation_id="UserCreate",
                         operation_summary='新增用户',
                         operation_description='',
                         responses={400011: "用户已存在",
                                    400012: "用户创建失败",
                                    400013: "请检查输入字段是否正确(必填字段、未定义字段)",
                                    400004: "密码长度需要8到20位",
                                    200: serializer_class})
    def create(self, request, *args, **kwargs):
        # 新增数据时，需要把入参同时存放到Account和UserDetail表，故先把入参按照models定义，拆分成两个字典，非上述表字段，不处理
        user_dict = {}
        detail_dict = {}
        for item in request.data.items():
            if item[0] in [field.name for field in Account._meta.get_fields()]:
                user_dict[item[0]] = item[1]
            elif item[0] in [field.name for field in UserDetail._meta.get_fields()]:
                detail_dict[item[0]] = item[1]

        # 检查账号密码是否有填写
        if "username" not in list(user_dict.keys()) or "password" not in list(user_dict.keys()):
            return APIResponse(400013, '请检查输入字段是否正确(必填字段、未定义字段)', success=False)
        else:
            if len(user_dict["password"]) > 20 or len(user_dict["password"]) < 8:
                return APIResponse(400004, '密码长度需要8到20位', success=False)

        if "email" in list(user_dict.keys()):
            detail_dict["user_email"] = user_dict["email"]

        # 检查用户是否存在
        try:
            Account.objects.get(username=request.data.get('username'))
            return APIResponse(400011, '用户已存在', success=False)
        except Account.DoesNotExist:
            # 如果不存在，先调用Account表新增数据
            try:
                user_create = Account.objects.update_or_create(defaults=user_dict, username=user_dict["username"])
                # 如果Account表新增数据成功，则通过外键user_id，在UserDetail新增对应的数据
                if user_create:
                    user_id = Account.objects.filter(username=user_dict["username"]).values('user_id').first()
                    UserDetail.objects.update_or_create(defaults=detail_dict, user_info_id=user_id["user_id"])
                    return APIResponse(200, '用户创建成功')
            except Exception as e:
                print(e)
                return APIResponse(400012, '用户创建失败', success=False)


class UserRoleView(viewsets.ModelViewSet):
    """用户登录信息"""
    queryset = UserRole.objects.filter().all()
    serializer_class = user_serializers.UserRoleSerializer
    filter_class = user_filter.UserRoleFilter
    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    ordering = ['-created_tm']


class LoginView(mixins.UpdateModelMixin, GenericAPIView):
    authentication_classes = ()
    permission_classes = ()

    queryset = Account.objects.filter(is_delete=0).all()
    serializer_class = user_serializers.LoginSerializer
    ordering = ['-created_tm']

    @swagger_auto_schema(tags=["用户"],
                         operation_id="Login",
                         operation_summary='用户登录',
                         operation_description='',
                         responses={400010: "账号密码错误",
                                    200: serializer_class
                                    })
    def post(self, request, *args, **kwargs):
        """
        post: 用户登录

        400010：账号密码错误
        """
        username = str(request.data.get('username'))
        password = str(request.data.get('password'))
        md5 = hashlib.md5()
        md5.update(password.encode())
        password = md5.hexdigest()

        try:
            Account.objects.get(username=username)
        except Account.DoesNotExist:
            return APIResponse(400010, '账号密码错误', success=False)

        try:
            Account.objects.get(password=password, username=username)
        except Account.DoesNotExist:
            return APIResponse(400010, '账号密码错误', success=False)

        user = Account.objects.filter(username=username, password=password).first()
        if user:
            # 登录成功，签发token,通过当前登录用户获取荷载（payload）
            payload = jwt_payload_handler(user)
            # 通过payload生成token串（三段：头，payload，签名）
            token = jwt_encode_handler(payload)
            UserRole.objects.update_or_create(defaults={'user_token': token}, user_info_id=user.user_id)
            response = {"user_id": user.user_id, "username": username, "token": token}
            return APIResponse(200, '登录成功', response)


class UpdatePasswordView(mixins.UpdateModelMixin, GenericAPIView):
    authentication_classes = [CustomJsonToken]
    permission_classes = (IsAuthenticated,)

    queryset = Account.objects.filter(is_delete=0).all()
    serializer_class = PasswordSerializer
    ordering = ['-created_tm']

    @swagger_auto_schema(tags=["用户"],
                         operation_id="UpdatePassword",
                         operation_summary='修改用户密码',
                         operation_description='',
                         responses={
                             400001: "用户不存在",
                             400002: "原密码输入不正确",
                             400003: "两次密码输入不一致",
                             400004: "密码长度需要8到20位",
                             400005: "新密码不能与原密码一致",
                             200: serializer_class
                         })
    def put(self, request, *args, **kwargs):
        """
        put: 修改用户密码

        400001：用户不存在

        400002：原密码输入不正确

        400003：两次密码输入不一致

        400004：密码长度需要8到20位

        400005：新密码不能与原密码一致
        """
        user_id = request.data.get('user_id')
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        md5 = hashlib.md5()
        md5.update(old_password.encode())
        old_password_md5 = md5.hexdigest()

        try:
            Account.objects.get(user_id=user_id)
        except Account.DoesNotExist:
            return APIResponse(400001, '用户不存在', success=False)

        try:
            Account.objects.filter(user_id=user_id).get(password=old_password_md5)
        except Account.DoesNotExist:
            return APIResponse(400002, '原密码输入不正确', success=False)

        if new_password != confirm_password:
            return APIResponse(400003, '两次密码输入不一致', success=False)

        if len(new_password) > 20 or len(new_password) < 8:
            return APIResponse(400004, '密码长度需要8到20位', success=False)

        if old_password == new_password:
            return APIResponse(400005, '新密码不能与原密码一致', success=False)

        user = Account.objects.filter(user_id=user_id, password=old_password_md5).first()
        if user:
            Account.objects.update_or_create(defaults={'password': new_password}, user_id=user_id)
            return APIResponse(200, '密码修改成功', {"user_id": user_id})
        return APIResponse(200, '密码修改成功', {"user_id": user_id})


class UserListView(mixins.ListModelMixin, generics.GenericAPIView):
    authentication_classes = [CustomJsonToken]
    permission_classes = (IsAuthenticated,)
    renderer_classes = [CustomerRenderer]

    queryset = Account.objects.filter(is_delete=False).all().order_by("-created_tm")
    serializer_class = user_serializers.UserListSerializer
    fields = ('user_id', 'username')
    filter_class = user_filter.UserFilter
    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)

    @swagger_auto_schema(tags=["用户"],
                         operation_id="UserList",
                         operation_summary='用户列表',
                         operation_description='',
                         responses={
                             400014: "参数错误",
                             200: serializer_class
                         })
    def post(self, request, *args, **kwargs):
        """
        post: 用户列表信息

        时间段查询需要传时间戳
        """
        try:
            user_id = request.data.get('user_id')
            username = request.data.get('username')
            email = request.data.get('email')
            created_start_time = request.data.get('created_start_tm')
            created_end_time = request.data.get('created_end_tm')
            page = request.data.get('page')
            size = request.data.get('size')
        except Exception:
            return APIResponse(400014, '参数错误', success=False)

        if page:  # 判断请求中是否有page和size参数
            request.query_params._mutable = True  # 让查询参数dict变为可编辑
            # query_params该参数会返回请求的查询参数，是个dict _mutable属性表示是否可编辑，默认是False
            request.query_params['page'] = page  # 添加page查询参数
            if size:
                request.query_params['size'] = size  # 添加size查询参数
            request.query_params._mutable = False  # 让查询参数dict变为不可编辑

        # 查询入参集合
        search_dict = {}

        if user_id:
            search_dict["user_id"] = user_id
        if username:
            search_dict["username__icontains"] = username
        if email:
            search_dict["email__icontains"] = email

        # 入参时间格式化
        if created_start_time and created_end_time:
            SearchTime().search_time_conversion(created_start_time, created_end_time, search_dict)

        # 由于覆盖了list方法，导致丢失了分页返回，故加上分页返回
        page_queryset = self.paginate_queryset(queryset=self.queryset.filter(**search_dict))

        # post请求加上分页条件查询
        if page_queryset is not None:
            serializer = self.get_serializer(page_queryset, many=True)
            return self.get_paginated_response(serializer.data)

        serializer_data = self.get_serializer(instance=page_queryset, many=True)

        return self.get_paginated_response(serializer_data.data)


class UserDisableView(mixins.UpdateModelMixin, generics.GenericAPIView):
    authentication_classes = [CustomJsonToken]
    permission_classes = (IsAuthenticated,)
    # authentication_classes = []
    # permission_classes = ()

    queryset = Account.objects.filter(is_delete=False).all()
    serializer_class = user_serializers.UserDisableSerializer

    @swagger_auto_schema(tags=["用户"],
                         operation_id="UserDisable",
                         operation_summary='用户禁用启用',
                         operation_description='1:启用；2:禁用',
                         responses={400011: "用户不存在",
                                    400015: "操作失败，用户状态不正确",
                                    200: serializer_class})
    def put(self, request, *args, **kwargs):
        try:
            user_id = request.data.get('user_id')
            is_disable = request.data.get('is_disable')
        except Exception:
            return APIResponse(400014, '参数错误', success=False)

        if is_disable == 1:
            is_disable = False
        elif is_disable == 2:
            is_disable = True
        else:
            return APIResponse(400014, '参数错误', success=False)

        try:
            Account.objects.get(user_id=user_id)
        except Account.DoesNotExist:
            return APIResponse(400001, '用户不存在', success=False)

        try:
            Account.objects.filter(user_id=user_id).get(is_disable=is_disable)
            return APIResponse(400015, '操作失败，用户状态不正确', success=False)
        except Account.DoesNotExist:
            user = Account.objects.filter(user_id=user_id).first()
            if user:
                Account.objects.update_or_create(defaults={'is_disable': is_disable}, user_id=user_id)
                return APIResponse(200, '操作成功')
        return APIResponse(200, '操作成功')
