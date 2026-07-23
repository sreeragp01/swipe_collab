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

    company = models.ForeignKey(
        "profiles.CompanyProfile",
        on_delete=models.CASCADE,
        related_name="projects",
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.CharField(max_length=20, choices=DURATION_CHOICES, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_OPEN)
    budget_min = models.DecimalField(max_digits=10, decimal_places=2)
    budget_max = models.DecimalField(max_digits=10, decimal_places=2)
    skills = models.ManyToManyField("profiles.Skill", blank=True, related_name="projects")
    deadline = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "projects_project"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} by {self.company.name}"


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
    proposed_rate = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "projects_application"
        unique_together = ("project", "freelancer")
        ordering = ["-created_at"]

    def __str__(self):
        return f"Application by {self.freelancer} → {self.project.title} [{self.status}]"