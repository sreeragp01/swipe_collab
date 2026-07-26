from rest_framework import serializers
from .models import Match, CollaborationSession, CollaborationRating
from users.serializers import UserSerializer


class MatchSerializer(serializers.ModelSerializer):
    other_user      = serializers.SerializerMethodField()
    partner         = serializers.SerializerMethodField()
    room_key        = serializers.SerializerMethodField()
    is_expired      = serializers.BooleanField(read_only=True)
    hours_remaining = serializers.SerializerMethodField()

    class Meta:
        model  = Match
        fields = [
            'id', 'user1', 'user2',
            'other_user', 'partner', 'room_key',
            'is_expired', 'hours_remaining',
            'created_at',
        ]

    def _build_user_payload(self, obj, request):
        if not request:
            return None
        other = obj.other_user(request.user)
        if not other:
            return None

        exact_name = None
        profile_id = None
        avatar_url = None

        if other.is_freelancer:
            try:
                prof = other.freelancer_profile
                exact_name = prof.full_name
                profile_id = str(prof.id)
                if prof.avatar:
                    avatar_url = prof.avatar.url
            except Exception:
                pass
        else:
            try:
                prof = other.company_profile
                exact_name = prof.company_name
                profile_id = str(prof.id)
                if prof.logo:
                    avatar_url = prof.logo.url
            except Exception:
                pass

        if not exact_name or not exact_name.strip():
            exact_name = other.get_full_name() or other.email.split('@')[0].capitalize()

        return {
            'id':          str(other.id),
            'user_id':     str(other.id),
            'profile_id':  profile_id,
            'email':       other.email,
            'role':        other.role,
            'name':        exact_name,
            'full_name':   exact_name,
            'avatar_url':  avatar_url,
        }

    def get_other_user(self, obj):
        request = self.context.get('request')
        return self._build_user_payload(obj, request)

    def get_partner(self, obj):
        request = self.context.get('request')
        return self._build_user_payload(obj, request)

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