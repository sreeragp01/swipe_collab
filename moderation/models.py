from django.conf import settings
from django.db import models


class Report(models.Model):
    CATEGORY_HARASSMENT = "harassment"
    CATEGORY_INAPPROPRIATE = "inappropriate_content"
    CATEGORY_FAKE_PROFILE = "fake_profile"
    CATEGORY_SPAM = "spam"
    CATEGORY_HATE_SPEECH = "hate_speech"
    CATEGORY_OTHER = "other"

    CATEGORY_CHOICES = [
        (CATEGORY_HARASSMENT, "Harassment"),
        (CATEGORY_INAPPROPRIATE, "Inappropriate Content"),
        (CATEGORY_FAKE_PROFILE, "Fake Profile"),
        (CATEGORY_SPAM, "Spam"),
        (CATEGORY_HATE_SPEECH, "Hate Speech"),
        (CATEGORY_OTHER, "Other"),
    ]

    STATUS_PENDING = "pending"
    STATUS_REVIEWED = "reviewed"
    STATUS_ACTIONED = "actioned"
    STATUS_DISMISSED = "dismissed"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending Review"),
        (STATUS_REVIEWED, "Reviewed"),
        (STATUS_ACTIONED, "Action Taken"),
        (STATUS_DISMISSED, "Dismissed"),
    ]

    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reports_filed",
    )
    reported_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reports_received",
    )
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default=CATEGORY_OTHER)
    reason = models.TextField(blank=True)
    evidence_url = models.URLField(blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default=STATUS_PENDING)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reports_reviewed",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "moderation_report"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Report#{self.pk} by {self.reporter} against {self.reported_user} [{self.status}]"


class BlockList(models.Model):
    blocker = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="blocked_users",
    )
    blocked = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="blocked_by_users",
    )
    reason = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "moderation_block_list"
        unique_together = ("blocker", "blocked")

    def __str__(self):
        return f"{self.blocker} blocked {self.blocked}"


class UserStrike(models.Model):
    STRIKE_LIMIT_WARN = 1
    STRIKE_LIMIT_TEMP_BAN = 2
    STRIKE_LIMIT_PERM_BAN = 3

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="strike",
    )
    strike_count = models.PositiveSmallIntegerField(default=0)
    is_temp_banned = models.BooleanField(default=False)
    temp_ban_until = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "moderation_user_strike"

    def __str__(self):
        return f"Strike({self.user.email}, count={self.strike_count})"

    def add_strike(self):
        self.strike_count += 1
        if self.strike_count >= self.STRIKE_LIMIT_PERM_BAN:
            self.user.is_active = False
            self.user.save(update_fields=["is_active"])
        self.save()