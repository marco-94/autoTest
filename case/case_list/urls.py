from django.urls import path, include
from case.case_list import views
from rest_framework import routers

router = routers.SimpleRouter()
router.register('case_create', views.CaseCreateViews, basename='CaseCreate')

urlpatterns = [
    path('', include(router.urls)),
    path('case_list', views.CaseListView.as_view()),
    path('case_edit', views.CaseEditViews.as_view()),
    path('case_disable', views.CaseDisableView.as_view()),
]
