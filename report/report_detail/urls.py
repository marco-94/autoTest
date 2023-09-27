from django.urls import path, include
from rest_framework import routers

router = routers.SimpleRouter()
# router.register('project_create', views.ProjectCreateViews, basename='ProjectCreate')

urlpatterns = [
    path('', include(router.urls)),
    # path('project_list', views.ProjectListView.as_view()),
    # path('project_edit', views.ProjectEditViews.as_view()),
    # path('project_disable', views.ProjectDisableView.as_view()),
    # path('project_create', views.AddProjectViews.as_view()),
]
