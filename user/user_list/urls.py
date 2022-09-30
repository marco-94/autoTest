from django.urls import path, include
from django.conf.urls import url
from user.user_list.views import UserListView, UserRoleView, LoginView, UpdatePasswordView, UserListV
from rest_framework import routers

router = routers.SimpleRouter()
router.register('list', UserListView, basename='userList')
router.register('role', UserRoleView, basename='userRole')
# router.register('user_l', UserListV, basename='ll')
# router.register('user_list', UserView, basename='user_list')

urlpatterns = [
    path('', include(router.urls)),
    url(r'log_in', LoginView.as_view()),
    url(r'user_list', UserListV.as_view()),
    url(r'update_password', UpdatePasswordView.as_view()),
]
