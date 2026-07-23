import uuid
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_FREELANCER = "freelancer"
    ROLE_COMPANY = "company"
    ROLE_CHOICES = [
        (ROLE_FREELANCER, "Freelancer"),
        (ROLE_COMPANY, "Company"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_FREELANCER)
    is_verified = models.BooleanField(default=False)
    face_verified = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)

    trial_started_at = models.DateTimeField(null=True, blank=True)
    trial_ends_at = models.DateTimeField(null=True, blank=True)
    is_trial_active = models.BooleanField(default=False)

    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "role"]

    class Meta:
        db_table = "users_user"
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return f"{self.email} ({self.role})"

    @property
    def is_freelancer(self):
        return self.role == self.ROLE_FREELANCER

    @property
    def is_company(self):
        return self.role == self.ROLE_COMPANY

    @property
    def trial_expired(self):
        if self.trial_ends_at is None:
            return False
        return timezone.now() > self.trial_ends_at

    @property
    def has_access(self):
        if self.is_company:
            return self.is_paid
        if self.is_freelancer:
            return self.is_paid or (self.is_trial_active and not self.trial_expired)
        return False

    @property
    def can_swipe(self):
        return self.is_verified and self.face_verified and self.has_access

    @property
    def full_name(self):
        name = self.get_full_name().strip()
        return name if name else self.email.split("@")[0]

    def start_trial(self):
        if self.is_freelancer and not self.trial_started_at:
            self.trial_started_at = timezone.now()
            self.trial_ends_at = timezone.now() + timedelta(days=30)
            self.is_trial_active = True
            self.save(update_fields=['trial_started_at', 'trial_ends_at', 'is_trial_active'])