from django.urls import path
from .views import ReportUserView, BlockUserView, UnblockUserView, AdminReportListView, AdminReportActionView

urlpatterns = [
    path('report/',                         ReportUserView.as_view(),       name='report-user'),
    path('block/',                          BlockUserView.as_view(),        name='block-user'),
    path('block/<str:blocked_id>/',         UnblockUserView.as_view(),      name='unblock-user'),
    path('admin/reports/',                  AdminReportListView.as_view(),  name='admin-report-list'),
    path('admin/reports/<int:report_id>/',  AdminReportActionView.as_view(), name='admin-report-action'),
]