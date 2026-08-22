from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ProfileView, EngagementStat
from .serializers import ProfileViewSerializer, EngagementStatSerializer

User = get_user_model()


class MyStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        stat, created = EngagementStat.objects.get_or_create(user=request.user)
        stat = sync_stats_for_user(request.user, stat)
        return Response(EngagementStatSerializer(stat).data)



class SyncMyStatsView(APIView):
    """
    Manually re-sync stats from actual database records.
    Call this after seeding test data or if stats look wrong.
    GET /api/v1/analytics/sync/
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        stat, _ = EngagementStat.objects.get_or_create(user=request.user)
        stat = sync_stats_for_user(request.user, stat)
        return Response({
            'message': 'Stats synced successfully.',
            'stats': EngagementStatSerializer(stat).data,
        })


def sync_stats_for_user(user, stat):
    """
    Recalculate all stats directly from database records.
    Works regardless of test mode or how data was created.
    """
    from swipe.models import SwipeAction
    from matches.models import Match, CollaborationRating
    from chat.models import Message
    from projects.models import Project, Application

    # Swipe stats
    stat.total_swipes_made = SwipeAction.objects.filter(
        swiper=user
    ).count()

    stat.total_likes_received = SwipeAction.objects.filter(
        target=user,
        action__in=[SwipeAction.ACTION_LIKE, SwipeAction.ACTION_SUPER_LIKE]
    ).count()

    stat.total_passes_received = SwipeAction.objects.filter(
        target=user,
        action=SwipeAction.ACTION_PASS
    ).count()

    # Match count
    stat.match_count = Match.objects.filter(
        Q(user1=user) | Q(user2=user)
    ).count()

    # Message count
    stat.message_count = Message.objects.filter(
        sender=user
    ).count()

    # Profile view count
    stat.profile_view_count = ProfileView.objects.filter(
        viewed_profile=user
    ).count()

    # Project stats
    if user.is_company:
        try:
            stat.projects_posted = Project.objects.filter(
                company__user=user
            ).count()
            stat.applications_received = Application.objects.filter(
                project__company__user=user
            ).count()
        except Exception:
            pass

    # Application stats
    if user.is_freelancer:
        try:
            stat.applications_sent = Application.objects.filter(
                freelancer__user=user
            ).count()
        except Exception:
            pass

    stat.save()
    return stat


class ProfileViewListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        views = ProfileView.objects.filter(
            viewed_profile=request.user
        ).order_by('-viewed_at')[:50]

        return Response({
            'total': ProfileView.objects.filter(viewed_profile=request.user).count(),
            'recent': ProfileViewSerializer(views, many=True).data,
        })


class RecordProfileViewView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        try:
            viewed_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {'detail': 'User not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        if viewed_user == request.user:
            return Response(
                {'detail': 'Cannot record view on yourself.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        ProfileView.objects.create(
            viewer=request.user,
            viewed_profile=viewed_user,
            source=request.data.get('source', 'swipe_feed'),
        )

        try:
            stat, _ = EngagementStat.objects.get_or_create(user=viewed_user)
            stat.profile_view_count += 1
            stat.save(update_fields=['profile_view_count'])
        except Exception:
            pass

        return Response(
            {'message': 'Profile view recorded.'},
            status=status.HTTP_201_CREATED,
        )


class AdminStatsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        total_users       = User.objects.count()
        total_freelancers = User.objects.filter(role='freelancer').count()
        total_companies   = User.objects.filter(role='company').count()
        paid_users        = User.objects.filter(is_paid=True).count()
        trial_users       = User.objects.filter(is_trial_active=True).count()

        return Response({
            'total_users':       total_users,
            'total_freelancers': total_freelancers,
            'total_companies':   total_companies,
            'paid_users':        paid_users,
            'trial_users':       trial_users,
        })