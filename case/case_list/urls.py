from django.urls import path, include
from case.case_list import views
from rest_framework import routers

router = routers.SimpleRouter()
# router.register('case_group_create', views.CaseGroupCreateViews, basename='CaseGroupCreate')

urlpatterns = [
    path('', include(router.urls)),
    # path('case_group_list', views.CaseGroupListView.as_view()),
    # path('case_group_edit', views.CaseGroupEditViews.as_view()),
    # path('case_group_disable', views.CaseGroupDisableView.as_view()),
]
