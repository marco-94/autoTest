from django.urls import path, include
from rest_framework import routers
from interface import views

router = routers.SimpleRouter()
# router.register('erp_login', views.ErpLoginView, basename='ErpLogin')

urlpatterns = [
    path('', include(router.urls)),
    path('erp_login', views.ErpLoginView.as_view()),
    path('interface_quick_test', views.InterfaceQuickTestView.as_view()),
    # path('case_group_disable', views.CaseGroupDisableView.as_view()),
]
