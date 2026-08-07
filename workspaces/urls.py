from django.urls import path
from workspaces.views import (
    WorkspaceListCreateView,
    WorkspaceDetailView,
    TaskListCreateView,
    TaskDetailView,
    WorkspaceFileListCreateView,
)

urlpatterns = [
    path('', WorkspaceListCreateView.as_view(), name='workspace-list-create'),
    path('<int:pk>/', WorkspaceDetailView.as_view(), name='workspace-detail'),
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('files/', WorkspaceFileListCreateView.as_view(), name='workspace-file-list-create'),
]
