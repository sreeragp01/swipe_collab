from rest_framework import serializers
from workspaces.models import Workspace, Task, WorkspaceFile
from users.serializers import UserPublicSerializer


class TaskSerializer(serializers.ModelSerializer):
    assigned_to_detail = UserPublicSerializer(source="assigned_to", read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "workspace",
            "assigned_to",
            "assigned_to_detail",
            "title",
            "description",
            "status",
            "priority",
            "deadline",
            "created_at",
            "updated_at",
        ]


class WorkspaceFileSerializer(serializers.ModelSerializer):
    uploaded_by_detail = UserPublicSerializer(source="uploaded_by", read_only=True)

    class Meta:
        model = WorkspaceFile
        fields = [
            "id",
            "workspace",
            "uploaded_by",
            "uploaded_by_detail",
            "title",
            "file_url",
            "file",
            "created_at",
        ]
        read_only_fields = ["uploaded_by", "created_at"]


class WorkspaceSerializer(serializers.ModelSerializer):
    owner_detail = UserPublicSerializer(source="owner", read_only=True)
    members_detail = UserPublicSerializer(source="members", many=True, read_only=True)
    tasks = TaskSerializer(many=True, read_only=True)
    files = WorkspaceFileSerializer(many=True, read_only=True)

    class Meta:
        model = Workspace
        fields = [
            "id",
            "project",
            "match",
            "title",
            "owner",
            "owner_detail",
            "members",
            "members_detail",
            "progress_percent",
            "status",
            "created_at",
            "updated_at",
            "tasks",
            "files",
        ]
        read_only_fields = ["owner", "created_at", "updated_at"]
