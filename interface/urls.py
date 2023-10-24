from django.urls import path, include, re_path
from rest_framework import routers
from interface import views
from django.conf import settings
from django.views.static import serve

router = routers.SimpleRouter()
# router.register('erp_login', views.ErpLoginView, basename='ErpLogin')

urlpatterns = [
    path('', include(router.urls)),
    re_path(r'media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    path('erp_login', views.ErpLoginView.as_view()),
    path('interface_quick_test', views.InterfaceQuickTestView.as_view()),
    path('oss_uploads', views.OssUploadsView.as_view()),
    path('oss_uploadsV2', views.OssUploadV2sView.as_view()),
]
