from django.urls import path, include
from rest_framework import routers
from report.report_list import views

router = routers.SimpleRouter()
router.register('report_create', views.ReportCreateViews, basename='ReportCreate')

urlpatterns = [
    path('', include(router.urls)),
    path('report_list', views.ReportListView.as_view()),
]
