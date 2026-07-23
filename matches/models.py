from datetime import timedelta
from django.conf import settings
from django.db import models
from django.utils import timezone


class Match(models.Model):
    EXPIRY_HOURS = 48

    user1 = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="matches_as_user1",
    )
    user2 = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="matches_as_user2",
    )
    expires_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Match expires if no message sent within 48 hours.",
    )
    is_expired = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "matches_match"
        unique_together = ("user1", "user2")
        ordering = ["-created_at"]

    def __str__(self):
        return f"Match({self.user1} ↔ {self.user2})"

    @classmethod
    def create(cls, user_a, user_b):
        uid_a, uid_b = str(user_a.pk), str(user_b.pk)
        if uid_a > uid_b:
            user_a, user_b = user_b, user_a
        return cls.objects.create(
            user1=user_a,
            user2=user_b,
            expires_at=timezone.now() + timedelta(hours=cls.EXPIRY_HOURS),
        )

    def other_user(self, user):
        return self.user2 if self.user1 == user else self.user1

    @property
    def hours_remaining(self):
        if self.is_expired or not self.expires_at:
            return 0
        delta = self.expires_at - timezone.now()
        return max(int(delta.total_seconds() / 3600), 0)

    def check_expiry(self):
        if not self.is_expired and self.expires_at and timezone.now() > self.expires_at:
            self.is_expired = True
            self.save(update_fields=["is_expired"])
        return self.is_expired

    def reset_expiry(self):
        self.expires_at = timezone.now() + timedelta(hours=self.EXPIRY_HOURS)
        self.is_expired = False
        self.save(update_fields=["expires_at", "is_expired"])


class CollaborationSession(models.Model):
    PLATFORM_MEET = "google_meet"
    PLATFORM_ZOOM = "zoom"

    PLATFORM_CHOICES = [
        (PLATFORM_MEET, "Google Meet"),
        (PLATFORM_ZOOM, "Zoom"),
    ]

    STATUS_SCHEDULED = "scheduled"
    STATUS_ONGOING = "ongoing"
    STATUS_COMPLETED = "completed"
    STATUS_CANCELLED = "cancelled"

    STATUS_CHOICES = [
        (STATUS_SCHEDULED, "Scheduled"),
        (STATUS_ONGOING, "Ongoing"),
        (STATUS_COMPLETED, "Completed"),
        (STATUS_CANCELLED, "Cancelled"),
    ]

    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name="collaboration_sessions")
    initiated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="initiated_sessions",
    )
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    meeting_link = models.URLField(blank=True)
    scheduled_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default=STATUS_SCHEDULED)
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "matches_collaboration_session"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Session #{self.pk} via {self.platform} [{self.status}]"


class CollaborationRating(models.Model):
    session = models.ForeignKey(
        CollaborationSession,
        on_delete=models.CASCADE,
        related_name="ratings",
    )
    rated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ratings_given",
    )
    rated_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ratings_received",
    )
    score = models.PositiveSmallIntegerField(
        help_text="1 to 5 star rating.",
    )
    review = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "matches_collab_rating"
        unique_together = ("session", "rated_by")

    def __str__(self):
        return f"Rating by {self.rated_by} → {self.rated_user}: {self.score}★"