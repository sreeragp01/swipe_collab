from rest_framework import serializers
from invitations.models import ProjectInvitation
from projects.serializers import ProjectSerializer
from users.serializers import UserPublicSerializer


class ProjectInvitationSerializer(serializers.ModelSerializer):
    sender_detail = UserPublicSerializer(source="sender", read_only=True)
    recipient_detail = UserPublicSerializer(source="recipient", read_only=True)
    project_detail = ProjectSerializer(source="project", read_only=True)

    class Meta:
        model = ProjectInvitation
        fields = [
            "id",
            "project",
            "sender",
            "recipient",
            "role_title",
            "proposed_budget",
            "message",
            "status",
            "created_at",
            "updated_at",
            "sender_detail",
            "recipient_detail",
            "project_detail",
        ]
        read_only_fields = ["sender", "status", "created_at", "updated_at"]
