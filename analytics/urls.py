from django.urls import path
from .views import (
    MyStatsView,
    SyncMyStatsView,
    ProfileViewListView,
    RecordProfileViewView,
    AdminStatsView,
)

urlpatterns = [
    path('me/',                          MyStatsView.as_view(),           name='my-stats'),
    path('sync/',                        SyncMyStatsView.as_view(),       name='sync-stats'),
    path('profile-views/',               ProfileViewListView.as_view(),   name='profile-views'),
    path('profile-views/<str:user_id>/', RecordProfileViewView.as_view(), name='record-profile-view'),
    path('admin/overview/',              AdminStatsView.as_view(),        name='admin-stats'),
]