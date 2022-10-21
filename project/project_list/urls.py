from django.urls import path, include
from project.project_list import views
from rest_framework import routers

router = routers.SimpleRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('project_list', views.ProjectListView.as_view()),
]
