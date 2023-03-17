from django.urls import path
from project.project_detail import views

urlpatterns = [
    path('project_detail', views.ProjectDetailView.as_view()),
]
