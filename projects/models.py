from django.conf import settings
from django.db import models


class Project(models.Model):
    STATUS_DRAFT = "draft"
    STATUS_OPEN = "open"
    STATUS_IN_PROGRESS = "in_progress"
    STATUS_COMPLETED = "completed"
    STATUS_CANCELLED = "cancelled"

    STATUS_CHOICES = [
        (STATUS_DRAFT, "Draft"),
        (STATUS_OPEN, "Open for Applications"),
        (STATUS_IN_PROGRESS, "In Progress"),
        (STATUS_COMPLETED, "Completed"),
        (STATUS_CANCELLED, "Cancelled"),
    ]

    DURATION_LESS_1_MONTH = "less_1_month"
    DURATION_1_3_MONTHS = "1_3_months"
    DURATION_3_6_MONTHS = "3_6_months"
    DURATION_6_PLUS = "6_plus_months"

    DURATION_CHOICES = [
        (DURATION_LESS_1_MONTH, "Less than 1 month"),
        (DURATION_1_3_MONTHS, "1 – 3 months"),
        (DURATION_3_6_MONTHS, "3 – 6 months"),
        (DURATION_6_PLUS, "6+ months"),
    ]

    TYPE_FIXED = "fixed_price"
    TYPE_HOURLY = "hourly"
    TYPE_CHOICES = [
        (TYPE_FIXED, "Fixed Price"),
        (TYPE_HOURLY, "Hourly Rate"),
    ]

    EXP_ENTRY = "entry"
    EXP_INTERMEDIATE = "intermediate"
    EXP_EXPERT = "expert"
    EXP_CHOICES = [
        (EXP_ENTRY, "Entry Level"),
        (EXP_INTERMEDIATE, "Intermediate"),
        (EXP_EXPERT, "Expert"),
    ]

    LOCATION_REMOTE = "remote"
    LOCATION_ONSITE = "onsite"
    LOCATION_HYBRID = "hybrid"
    LOCATION_CHOICES = [
        (LOCATION_REMOTE, "Remote"),
        (LOCATION_ONSITE, "On-site"),
        (LOCATION_HYBRID, "Hybrid"),
    ]

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_projects",
        null=True,
        blank=True,
    )
    company = models.ForeignKey(
        "profiles.CompanyProfile",
        on_delete=models.CASCADE,
        related_name="projects",
        null=True,
        blank=True,
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=100, blank=True, default="Software Development")
    project_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=TYPE_FIXED)
    experience_level = models.CharField(max_length=20, choices=EXP_CHOICES, default=EXP_INTERMEDIATE)
    location_type = models.CharField(max_length=20, choices=LOCATION_CHOICES, default=LOCATION_REMOTE)
    duration = models.CharField(max_length=20, choices=DURATION_CHOICES, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_OPEN, db_index=True)
    budget_min = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    budget_max = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    skills = models.ManyToManyField("profiles.Skill", blank=True, related_name="projects")
    deadline = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "projects_project"
        ordering = ["-created_at"]

    def __str__(self):
        owner_name = self.owner.email if self.owner else (self.company.name if self.company else "Unknown")
        return f"{self.title} by {owner_name}"


class Application(models.Model):
    STATUS_PENDING = "pending"
    STATUS_SHORTLISTED = "shortlisted"
    STATUS_ACCEPTED = "accepted"
    STATUS_REJECTED = "rejected"
    STATUS_WITHDRAWN = "withdrawn"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_SHORTLISTED, "Shortlisted"),
        (STATUS_ACCEPTED, "Accepted"),
        (STATUS_REJECTED, "Rejected"),
        (STATUS_WITHDRAWN, "Withdrawn"),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="applications")
    freelancer = models.ForeignKey(
        "profiles.FreelancerProfile",
        on_delete=models.CASCADE,
        related_name="applications",
    )
    cover_letter = models.TextField(blank=True)
    proposed_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estimated_days = models.PositiveIntegerField(default=30)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "projects_application"
        unique_together = ("project", "freelancer")
        ordering = ["-created_at"]

    def __str__(self):
        return f"Application by {self.freelancer} → {self.project.title} [{self.status}]"