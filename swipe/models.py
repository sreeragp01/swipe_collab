from django.conf import settings
from django.db import models
from django.utils import timezone


class SwipeAction(models.Model):
    ACTION_LIKE = "like"
    ACTION_PASS = "pass"
    ACTION_SUPER_LIKE = "super_like"

    ACTION_CHOICES = [
        (ACTION_LIKE, "Like"),
        (ACTION_PASS, "Pass"),
        (ACTION_SUPER_LIKE, "Super Like"),
    ]

    swiper = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="swipes_made",
    )
    target = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="swipes_received",
    )
    action = models.CharField(max_length=15, choices=ACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "swipe_action"
        unique_together = ("swiper", "target")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=['swiper', 'action']),
            models.Index(fields=['target', 'action']),
            models.Index(fields=['swiper', 'target']),
        ]

    def __str__(self):
        return f"{self.swiper} → {self.target} [{self.action}]"

    @classmethod
    def is_mutual_like(cls, user_a, user_b):
        return cls.objects.filter(
            swiper=user_a, target=user_b, action=cls.ACTION_LIKE
        ).exists() and cls.objects.filter(
            swiper=user_b, target=user_a, action=cls.ACTION_LIKE
        ).exists()

    @classmethod
    def super_likes_used_today(cls, user):
        today = timezone.now().date()
        return cls.objects.filter(
            swiper=user,
            action=cls.ACTION_SUPER_LIKE,
            created_at__date=today,
        ).count()

    @classmethod
    def can_super_like(cls, user):
        DAILY_LIMIT = 3
        return cls.super_likes_used_today(user) < DAILY_LIMIT


class SwipeFilter(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="swipe_filters",
    )
    experience_min = models.PositiveSmallIntegerField(default=0)
    experience_max = models.PositiveSmallIntegerField(default=30)
    required_skills = models.ManyToManyField(
        "profiles.Skill",
        blank=True,
        related_name="swipe_filters",
    )
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    availability = models.CharField(max_length=20, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "swipe_filter"

    def __str__(self):
        return f"Filter for {self.user}"


class SkillMatchScore(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="skill_scores_given",
    )
    target = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="skill_scores_received",
    )
    score = models.PositiveSmallIntegerField(
        default=0,
        help_text="0-100 percentage overlap of skills between user and target.",
    )
    calculated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "swipe_skill_match_score"
        unique_together = ("user", "target")

    def __str__(self):
        return f"SkillMatch({self.user} → {self.target}: {self.score}%)"

    @staticmethod
    def calculate(user, target):
        try:
            if user.is_freelancer:
                user_skills = set(user.freelancer_profile.skills.values_list("id", flat=True))
                target_skills = set(target.company_profile.skills.values_list("id", flat=True))
            else:
                user_skills = set(user.company_profile.skills.values_list("id", flat=True))
                target_skills = set(target.freelancer_profile.skills.values_list("id", flat=True))

            if not user_skills or not target_skills:
                return 0

            overlap = len(user_skills & target_skills)
            total = len(user_skills | target_skills)
            return int((overlap / total) * 100) if total > 0 else 0
        except Exception:
            return 0