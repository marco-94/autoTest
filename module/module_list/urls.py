from django.urls import path, include
from module.module_list import views
from rest_framework import routers

router = routers.SimpleRouter()
router.register('module_create', views.ModuleCreateViews, basename='ModuleCreate')

urlpatterns = [
    path('', include(router.urls)),
    path('module_list', views.ModuleListView.as_view()),
    path('module_edit', views.ModuleEditViews.as_view()),
    path('module_disable', views.ModuleDisableView.as_view()),
]
