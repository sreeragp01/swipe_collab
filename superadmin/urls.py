from django.urls import path
from .views import (
    SuperAdminOverviewView,
    SuperAdminUserListView,
    SuperAdminUserDetailView,
    SuperAdminProjectListView,
    SuperAdminProjectDetailView,
    SuperAdminReportListView,
    SuperAdminReportActionView,
    SuperAdminPaymentListView,
)

urlpatterns = [
    path('overview/',             SuperAdminOverviewView.as_view(),      name='superadmin-overview'),
    path('users/',                SuperAdminUserListView.as_view(),      name='superadmin-user-list'),
    path('users/<uuid:pk>/',      SuperAdminUserDetailView.as_view(),    name='superadmin-user-detail'),
    path('projects/',             SuperAdminProjectListView.as_view(),   name='superadmin-project-list'),
    path('projects/<int:pk>/',    SuperAdminProjectDetailView.as_view(), name='superadmin-project-detail'),
    path('reports/',              SuperAdminReportListView.as_view(),    name='superadmin-report-list'),
    path('reports/<int:pk>/',     SuperAdminReportActionView.as_view(),  name='superadmin-report-action'),
    path('payments/',             SuperAdminPaymentListView.as_view(),   name='superadmin-payment-list'),
]
