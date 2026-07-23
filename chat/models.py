import uuid
from django.conf import settings
from django.db import models


class ChatRoom(models.Model):
    match = models.OneToOneField(
        "matches.Match",
        on_delete=models.CASCADE,
        related_name="chat_room",
    )
    room_key = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "chat_room"

    def __str__(self):
        return f"ChatRoom({self.room_key})"

    @property
    def channel_group_name(self):
        return f"chat_{self.room_key.hex}"

    def unread_count_for(self, user):
        return self.messages.filter(is_read=False).exclude(sender=user).count()


class Message(models.Model):
    MESSAGE_TYPE_TEXT = "text"
    MESSAGE_TYPE_FILE = "file"
    MESSAGE_TYPE_IMAGE = "image"

    MESSAGE_TYPE_CHOICES = [
        (MESSAGE_TYPE_TEXT, "Text"),
        (MESSAGE_TYPE_FILE, "File"),
        (MESSAGE_TYPE_IMAGE, "Image"),
    ]

    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="messages_sent",
    )
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPE_CHOICES, default=MESSAGE_TYPE_TEXT)
    content = models.TextField(blank=True)
    file = models.FileField(upload_to="chat/files/", blank=True, null=True)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "chat_message"
        ordering = ["created_at"]

    def __str__(self):
        return f"Msg#{self.pk} by {self.sender} in Room({self.room.room_key})"

    def mark_read(self):
        from django.utils import timezone
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=["is_read", "read_at"])


class MessageReaction(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="reactions")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="message_reactions",
    )
    emoji = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "chat_message_reaction"
        unique_together = ("message", "user")

    def __str__(self):
        return f"{self.user} reacted {self.emoji} to Msg#{self.message_id}"