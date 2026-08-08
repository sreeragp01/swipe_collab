import uuid
from django.conf import settings
from django.db import models


class Notification(models.Model):
    TYPE_INTEREST_SENT = 'interest_sent'
    TYPE_INTEREST_RECEIVED = 'interest_received'
    TYPE_MATCH_MADE = 'match_made'
    TYPE_CHAT_MESSAGE = 'chat_message'
    TYPE_PORTFOLIO_LIKE = 'portfolio_like'
    TYPE_PORTFOLIO_COMMENT = 'portfolio_comment'
    TYPE_SYSTEM = 'system'

    TYPE_CHOICES = [
        (TYPE_INTEREST_SENT, 'Interest Sent'),
        (TYPE_INTEREST_RECEIVED, 'Interest Received'),
        (TYPE_MATCH_MADE, 'Match Made'),
        (TYPE_CHAT_MESSAGE, 'Chat Message Received'),
        (TYPE_PORTFOLIO_LIKE, 'Portfolio Item Liked'),
        (TYPE_PORTFOLIO_COMMENT, 'Portfolio Item Commented'),
        (TYPE_SYSTEM, 'System Notification'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sent_notifications',
    )
    notification_type = models.CharField(max_length=50, choices=TYPE_CHOICES, default=TYPE_SYSTEM)
    title = models.CharField(max_length=255)
    message = models.TextField()
    link = models.CharField(max_length=255, blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notifications_notification'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read']),
            models.Index(fields=['user', '-created_at']),
        ]

    def __str__(self):
        return f"Notification for {self.user.email}: {self.title}"


def notify_user(user, notification_type, title, message, sender=None, link=None):
    try:
        return Notification.objects.create(
            user=user,
            sender=sender,
            notification_type=notification_type,
            title=title,
            message=message,
            link=link,
        )
    except Exception as e:
        print(f"Error creating notification: {e}")
        return None
