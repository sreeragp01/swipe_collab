# pyrefly: ignore [missing-import]
from rest_framework import serializers
from .models import ChatRoom, Message


class MessageSerializer(serializers.ModelSerializer):
    sender_email = serializers.EmailField(source='sender.email', read_only=True)
    sender_username = serializers.CharField(source='sender.username', read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'room', 'sender', 'sender_email', 'sender_username', 'message_type', 'content', 'file', 'is_read', 'created_at']
        read_only_fields = ['id', 'sender', 'is_read', 'created_at']


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
        if not request or not hasattr(request, 'user') or not request.user or not request.user.is_authenticated:
            return None
        other = obj.match.other_user(request.user)
        if not other:
            return None
        username = other.username if other.username else (other.get_full_name() or other.email.split('@')[0])
        return {
            'id': str(other.id),
            'username': username,
            'email': other.email,
            'role': other.role,
            'display_name': username,
        }