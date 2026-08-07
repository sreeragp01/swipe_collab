from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from workspaces.models import Workspace, Task, WorkspaceFile
from workspaces.serializers import (
    WorkspaceSerializer,
    TaskSerializer,
    WorkspaceFileSerializer,
)


class WorkspaceListCreateView(generics.ListCreateAPIView):
    serializer_class = WorkspaceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Workspace.objects.filter(members=user) | Workspace.objects.filter(owner=user)

    def perform_create(self, serializer):
        workspace = serializer.save(owner=self.request.user)
        workspace.members.add(self.request.user)


class WorkspaceDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WorkspaceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Workspace.objects.filter(members=user) | Workspace.objects.filter(owner=user)


class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        workspace_id = self.request.query_params.get("workspace_id")
        if workspace_id:
            return Task.objects.filter(workspace_id=workspace_id)
        return Task.objects.none()

    def perform_create(self, serializer):
        task = serializer.save()
        task.workspace.recalculate_progress()


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Task.objects.all()

    def perform_update(self, serializer):
        task = serializer.save()
        task.workspace.recalculate_progress()


class WorkspaceFileListCreateView(generics.ListCreateAPIView):
    serializer_class = WorkspaceFileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        workspace_id = self.request.query_params.get("workspace_id")
        if workspace_id:
            return WorkspaceFile.objects.filter(workspace_id=workspace_id)
        return WorkspaceFile.objects.none()

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)
