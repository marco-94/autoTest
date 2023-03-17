from django.urls import path, include
from django.conf.urls import url
from user.user_list import views
from rest_framework import routers

router = routers.SimpleRouter()
router.register('user_create', views.UserCreateView, basename='userCreate')
# router.register('role', UserRoleView, basename='userRole')
# router.register('user_l', UserListV, basename='ll')
# router.register('user_list', UserView, basename='user_list')

urlpatterns = [
    path('', include(router.urls)),
    url(r'log_in', views.LoginView.as_view()),
    url(r'user_list', views.UserListView.as_view()),
    url(r'update_password', views.UpdatePasswordView.as_view()),
    url(r'user_disable', views.UserDisableView.as_view()),
]
