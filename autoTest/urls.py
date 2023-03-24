"""autoTest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework.documentation import include_docs_urls
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token

schema_view = get_schema_view(
    openapi.Info(
        title="API接口文档平台",  # 必传
        default_version='beta-v1',  # 必传
        description="这是一个接口文档",
        terms_of_service="",
        contact=openapi.Contact(email=""),
        license=openapi.License(name=""),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=(),
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # 接口文档：swagger
    path('docs/', include_docs_urls(title='测试平台接口文档', description='xxx描述')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    # 映射子项目路由
    path('user/', include('user.user_list.urls')),
    path('user/', include('user.user_detail.urls')),

    path('project/', include('project.project_list.urls')),
    path('project/', include('project.project_detail.urls')),

    path('module/', include('module.module_list.urls')),
    path('module/', include('module.module_detail.urls')),

    path('case_group/', include('caseGroup.urls')),

    path('case/', include('case.case_list.urls')),

    # token
    # 签发token
    # path('login/', obtain_jwt_token),
    # 校验token
    # path('verify/', verify_jwt_token),
    # 刷新token
    # path('refresh/', refresh_jwt_token),
]
