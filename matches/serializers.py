from rest_framework import serializers
from .models import Match, CollaborationSession, CollaborationRating
from users.serializers import UserSerializer


class MatchSerializer(serializers.ModelSerializer):
    other_user  = serializers.SerializerMethodField()
    room_key    = serializers.SerializerMethodField()
    is_expired      = serializers.BooleanField(read_only=True)
    hours_remaining = serializers.SerializerMethodField()

    class Meta:
        model  = Match
        fields = [
            'id', 'user1', 'user2',
            'other_user', 'room_key',
            'is_expired', 'hours_remaining',
            'created_at',
        ]

    def get_other_user(self, obj):
        request = self.context.get('request')
        if not request:
            return None
        other = obj.other_user(request.user)
        if not other:
            return None
        return {
            'id':       str(other.id),
            'email':    other.email,
            'role':     other.role,
            'full_name': other.get_full_name() or other.email.split('@')[0],
        }

    def get_room_key(self, obj):
        try:
            return str(obj.chat_room.room_key)
        except Exception:
            return None

    def get_hours_remaining(self, obj):
        return obj.hours_remaining


class CollaborationSessionSerializer(serializers.ModelSerializer):
    initiated_by = UserSerializer(read_only=True)

    class Meta:
        model  = CollaborationSession
        fields = [
            'id', 'match', 'initiated_by', 'platform',
            'meeting_link', 'scheduled_at', 'status',
            'started_at', 'ended_at', 'created_at',
        ]
        read_only_fields = ['id', 'initiated_by', 'created_at']


class CreateCollaborationSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model  = CollaborationSession
        fields = ['platform', 'meeting_link', 'scheduled_at']


class CollaborationRatingSerializer(serializers.ModelSerializer):
    rated_by_email   = serializers.EmailField(source='rated_by.email',   read_only=True)
    rated_user_email = serializers.EmailField(source='rated_user.email', read_only=True)

    class Meta:
        model  = CollaborationRating
        fields = ['id', 'session', 'rated_by_email', 'rated_user_email', 'score', 'review', 'created_at']
        read_only_fields = ['id', 'rated_by_email', 'rated_user_email', 'created_at']