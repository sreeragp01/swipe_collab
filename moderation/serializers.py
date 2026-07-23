from rest_framework import serializers
from .models import Report, BlockList, UserStrike


class ReportSerializer(serializers.ModelSerializer):
    reporter_email = serializers.EmailField(source='reporter.email', read_only=True)
    reported_email = serializers.EmailField(source='reported_user.email', read_only=True)

    class Meta:
        model = Report
        fields = [
            'id', 'reporter_email', 'reported_user', 'reported_email',
            'category', 'reason', 'evidence_url', 'status',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'reporter_email', 'reported_email', 'status', 'created_at', 'updated_at']


class BlockListSerializer(serializers.ModelSerializer):
    blocker_email = serializers.EmailField(source='blocker.email', read_only=True)
    blocked_email = serializers.EmailField(source='blocked.email', read_only=True)

    class Meta:
        model = BlockList
        fields = ['id', 'blocker_email', 'blocked', 'blocked_email', 'reason', 'created_at']
        read_only_fields = ['id', 'blocker_email', 'blocked_email', 'created_at']


class UserStrikeSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = UserStrike
        fields = ['id', 'user_email', 'strike_count', 'is_temp_banned', 'temp_ban_until', 'notes', 'updated_at']
        read_only_fields = ['id', 'user_email', 'updated_at']