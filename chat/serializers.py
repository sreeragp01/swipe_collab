# pyrefly: ignore [missing-import]
from rest_framework import serializers
from .models import ChatRoom, Message


class MessageSerializer(serializers.ModelSerializer):
    sender_email = serializers.EmailField(source='sender.email', read_only=True)
    sender_username = serializers.CharField(source='sender.username', read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'room', 'sender', 'sender_email', 'sender_username', 'message_type', 'content', 'file', 'is_read', 'is_deleted', 'created_at']
        read_only_fields = ['id', 'room', 'sender', 'is_read', 'is_deleted', 'created_at']




class ChatRoomSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()
    match_id = serializers.IntegerField(source='match.id', read_only=True)
    other_user = serializers.SerializerMethodField()

    class Meta:
        model = ChatRoom
        fields = ['id', 'match_id', 'room_key', 'last_message', 'unread_count', 'other_user', 'created_at']

    def get_last_message(self, obj):
        last = obj.messages.last()
        if last:
            return MessageSerializer(last).data
        return None

    def get_unread_count(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user and request.user.is_authenticated:
            return obj.messages.filter(is_read=False).exclude(sender=request.user).count()
        return 0

    def get_other_user(self, obj):
        request = self.context.get('request')
        other = None
        if request and hasattr(request, 'user') and request.user and request.user.is_authenticated:
            other = obj.match.other_user(request.user)
        if not other:
            other = obj.match.user2

        if not other:
            return None

        exact_name = None
        avatar_url = None
        if hasattr(other, 'is_freelancer') and other.is_freelancer:
            try:
                prof = getattr(other, 'freelancer_profile', None)
                if prof:
                    exact_name = prof.full_name
                    if prof.avatar:
                        avatar_url = prof.avatar.url
            except Exception:
                pass
        else:
            try:
                prof = getattr(other, 'company_profile', None)
                if prof:
                    exact_name = prof.company_name
                    if prof.logo:
                        avatar_url = prof.logo.url
            except Exception:
                pass

        if not exact_name or not exact_name.strip():
            exact_name = getattr(other, 'username', None) or getattr(other, 'email', 'Collaborator').split('@')[0]

        return {
            'id': str(other.id),
            'username': getattr(other, 'username', exact_name),
            'email': getattr(other, 'email', ''),
            'role': getattr(other, 'role', 'freelancer'),
            'display_name': exact_name,
            'avatar_url': avatar_url,
        }