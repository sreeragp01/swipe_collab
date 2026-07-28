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
    portfolio_style = models.CharField(max_length=50, default="modern_glass", blank=True)
    portfolio_custom_data = models.JSONField(default=dict, blank=True)
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


class PortfolioItem(models.Model):
    freelancer = models.ForeignKey(
        FreelancerProfile,
        on_delete=models.CASCADE,
        related_name="portfolio_items",
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    experience_gained = models.TextField(blank=True)
    media_file = models.FileField(upload_to="portfolio_media/", blank=True, null=True)
    project_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "profiles_portfolio_item"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} by {self.freelancer.name}"


class PortfolioItemLike(models.Model):
    item = models.ForeignKey(
        PortfolioItem,
        on_delete=models.CASCADE,
        related_name="likes",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="portfolio_likes",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "profiles_portfolio_like"
        unique_together = ("item", "user")

    def __str__(self):
        return f"{self.user.email} liked {self.item.title}"


class PortfolioItemComment(models.Model):
    item = models.ForeignKey(
        PortfolioItem,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="portfolio_comments",
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "profiles_portfolio_comment"
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.user.email} on {self.item.title}: {self.text[:30]}"