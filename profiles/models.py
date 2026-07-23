from django.conf import settings
from django.db import models


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=100, blank=True)

    class Meta:
        db_table = "profiles_skill"
        ordering = ["name"]

    def __str__(self):
        return self.name


class FreelancerProfile(models.Model):
    AVAILABILITY_FULL_TIME = "full_time"
    AVAILABILITY_PART_TIME = "part_time"
    AVAILABILITY_CONTRACT = "contract"
    AVAILABILITY_NOT_AVAILABLE = "not_available"

    AVAILABILITY_CHOICES = [
        (AVAILABILITY_FULL_TIME, "Full Time"),
        (AVAILABILITY_PART_TIME, "Part Time"),
        (AVAILABILITY_CONTRACT, "Contract / Freelance"),
        (AVAILABILITY_NOT_AVAILABLE, "Not Available"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="freelancer_profile",
    )
    name = models.CharField(max_length=255)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="avatars/freelancers/", blank=True, null=True)
    portfolio_url = models.URLField(blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    experience_years = models.PositiveSmallIntegerField(default=0)
    availability = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES, default=AVAILABILITY_FULL_TIME)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    skills = models.ManyToManyField(Skill, blank=True, related_name="freelancers")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "profiles_freelancer"

    def __str__(self):
        return f"Freelancer: {self.name} ({self.user.email})"


class CompanyProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="company_profile",
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to="avatars/companies/", blank=True, null=True)
    website_url = models.URLField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    skills = models.ManyToManyField(Skill, blank=True, related_name="companies")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "profiles_company"

    def __str__(self):
        return f"Company: {self.name} ({self.user.email})"