from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from invitations.models import ProjectInvitation
from invitations.serializers import ProjectInvitationSerializer
from matches.models import Match
from workspaces.models import Workspace
from notifications.models import notify_user, Notification


class InvitationListCreateView(generics.ListCreateAPIView):
    serializer_class = ProjectInvitationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ProjectInvitation.objects.filter(sender=user) | ProjectInvitation.objects.filter(recipient=user)

    def perform_create(self, serializer):
        invitation = serializer.save(sender=self.request.user)
        # Send notification to recipient
        notify_user(
            user=invitation.recipient,
            notification_type=Notification.TYPE_SYSTEM,
            title="New Project Invitation 🚀",
            message=f"{self.request.user.first_name or self.request.user.email} invited you to project '{invitation.project.title}'",
            sender=self.request.user,
            link="/discover/",
        )


class ReceivedInvitationsListView(generics.ListAPIView):
    serializer_class = ProjectInvitationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ProjectInvitation.objects.filter(recipient=self.request.user, status=ProjectInvitation.STATUS_PENDING)


class RespondInvitationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        invitation = get_object_or_404(ProjectInvitation, pk=pk, recipient=request.user)
        action = request.data.get("action")

        if action == "accept":
            invitation.status = ProjectInvitation.STATUS_ACCEPTED
            invitation.save()

            match = Match.create(
                user_a=invitation.sender,
                user_b=invitation.recipient,
                match_type=Match.MATCH_INVITATION,
                project=invitation.project,
            )

            workspace, _ = Workspace.objects.get_or_create(
                project=invitation.project,
                match=match,
                defaults={
                    "title": f"Workspace: {invitation.project.title}",
                    "owner": invitation.sender,
                }
            )
            workspace.members.add(invitation.sender, invitation.recipient)

            notify_user(
                user=invitation.sender,
                notification_type=Notification.TYPE_MATCH_MADE,
                title="Invitation Accepted! 🎉",
                message=f"{request.user.first_name or request.user.email} accepted your invitation to '{invitation.project.title}'! Workspace created.",
                sender=request.user,
                link="/workspace/",
            )

            return Response({
                "message": "Invitation accepted successfully! Workspace created.",
                "invitation": ProjectInvitationSerializer(invitation).data,
                "match_id": match.id,
                "workspace_id": workspace.id,
            }, status=status.HTTP_200_OK)

        elif action == "decline":
            invitation.status = ProjectInvitation.STATUS_DECLINED
            invitation.save()

            notify_user(
                user=invitation.sender,
                notification_type=Notification.TYPE_SYSTEM,
                title="Invitation Declined",
                message=f"{request.user.first_name or request.user.email} declined your invitation to '{invitation.project.title}'",
                sender=request.user,
                link="/discover/",
            )

            return Response({
                "message": "Invitation declined.",
                "invitation": ProjectInvitationSerializer(invitation).data,
            }, status=status.HTTP_200_OK)

        return Response({"error": "Invalid action. Use 'accept' or 'decline'."}, status=status.HTTP_400_BAD_REQUEST)
