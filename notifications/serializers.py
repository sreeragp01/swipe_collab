from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField()
    sender_avatar = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = [
            'id', 'notification_type', 'title', 'message',
            'link', 'is_read', 'created_at',
            'sender', 'sender_name', 'sender_avatar',
        ]
        read_only_fields = ['id', 'created_at']

    def get_sender_name(self, obj):
        if not obj.sender:
            return 'SwipeCollab System'
        if hasattr(obj.sender, 'freelancer_profile'):
            return obj.sender.freelancer_profile.name
        if hasattr(obj.sender, 'company_profile'):
            return obj.sender.company_profile.name
        return obj.sender.full_name

    def get_sender_avatar(self, obj):
        if not obj.sender:
            return None
        if hasattr(obj.sender, 'freelancer_profile') and obj.sender.freelancer_profile.avatar:
            return obj.sender.freelancer_profile.avatar.url
        if hasattr(obj.sender, 'company_profile') and obj.sender.company_profile.logo:
            return obj.sender.company_profile.logo.url
        return None
