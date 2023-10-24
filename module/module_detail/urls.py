from django.urls import path
from module.module_detail import views

urlpatterns = [
    path('module_detail', views.ModuleDetailView.as_view()),
]
