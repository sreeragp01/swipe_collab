from rest_framework import serializers
from .models import ProfileView, EngagementStat


class ProfileViewSerializer(serializers.ModelSerializer):
    viewer_email = serializers.EmailField(source='viewer.email', read_only=True)
    viewed_email = serializers.EmailField(source='viewed_profile.email', read_only=True)

    class Meta:
        model = ProfileView
        fields = ['id', 'viewer_email', 'viewed_email', 'source', 'viewed_at']


class EngagementStatSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = EngagementStat
        fields = [
            'id', 'user_email',
            'total_swipes_made', 'total_likes_received', 'total_passes_received',
            'match_count', 'message_count', 'profile_view_count',
            'projects_posted', 'applications_received', 'applications_sent',
            'updated_at',
        ]
        read_only_fields = fields