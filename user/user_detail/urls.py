from django.urls import path, include
from user.user_detail import views
from rest_framework import routers

router = routers.SimpleRouter()
# router.register('detail', views.UserDetailView, basename='userDetail')

urlpatterns = [
    path('', include(router.urls)),
    path('user_detail', views.UserDetailViewV2.as_view()),
]
