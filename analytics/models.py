from django.conf import settings
from django.db import models


class ProfileView(models.Model):
    viewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profiles_viewed",
    )
    viewed_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile_views",
    )
    source = models.CharField(max_length=30, blank=True)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "analytics_profile_view"
        ordering = ["-viewed_at"]

    def __str__(self):
        return f"{self.viewer} viewed {self.viewed_profile} at {self.viewed_at:%Y-%m-%d %H:%M}"


class EngagementStat(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="engagement_stats",
    )
    total_swipes_made = models.PositiveIntegerField(default=0)
    total_likes_received = models.PositiveIntegerField(default=0)
    total_passes_received = models.PositiveIntegerField(default=0)
    match_count = models.PositiveIntegerField(default=0)
    message_count = models.PositiveIntegerField(default=0)
    profile_view_count = models.PositiveIntegerField(default=0)
    projects_posted = models.PositiveIntegerField(default=0)
    applications_received = models.PositiveIntegerField(default=0)
    applications_sent = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "analytics_engagement_stat"

    def __str__(self):
        return f"Stats({self.user.email})"

    def increment(self, field_name, amount=1):
        from django.db.models import F
        EngagementStat.objects.filter(pk=self.pk).update(
            **{field_name: F(field_name) + amount}
        )
        self.refresh_from_db(fields=[field_name])