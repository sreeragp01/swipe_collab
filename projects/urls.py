from django.urls import path
from .views import (
    ProjectListView, ProjectCreateView, ProjectDetailView,
    MyProjectsView, ApplicationListView, ApplicationStatusView, MyApplicationsView,
)

urlpatterns = [
    path('',                                                    ProjectListView.as_view(),       name='project-list'),
    path('create/',                                             ProjectCreateView.as_view(),     name='project-create'),
    path('mine/',                                               MyProjectsView.as_view(),        name='project-mine'),
    path('<int:pk>/',                                           ProjectDetailView.as_view(),     name='project-detail'),
    path('<int:project_id>/applications/',                      ApplicationListView.as_view(),   name='application-list'),
    path('<int:project_id>/applications/<int:application_id>/', ApplicationStatusView.as_view(), name='application-status'),
    path('applications/mine/',                                  MyApplicationsView.as_view(),    name='application-mine'),
]