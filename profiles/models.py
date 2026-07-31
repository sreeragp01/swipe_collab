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
    title = models.CharField(max_length=255, blank=True, default="")
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="avatars/freelancers/", blank=True, null=True)
    avatar_data = models.TextField(blank=True, default="")
    portfolio_url = models.URLField(blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    video_intro_url = models.URLField(blank=True, null=True)
    portfolio_style = models.CharField(max_length=50, default="modern_glass", blank=True)
    portfolio_custom_data = models.JSONField(default=dict, blank=True)
    experience_years = models.PositiveSmallIntegerField(default=0)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    hours_per_week = models.CharField(max_length=50, blank=True, default="more_than_30")
    english_fluency = models.CharField(max_length=50, default="fluent", blank=True)
    education = models.JSONField(default=list, blank=True)
    certifications = models.JSONField(default=list, blank=True)
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

    def get_avatar_url(self):
        if self.avatar_data and self.avatar_data.strip():
            return self.avatar_data
        if self.avatar:
            try:
                return self.avatar.url
            except Exception:
                pass
        return None

    def get_completeness_score(self):
        score = 0
        checklist = []

        # 1. Avatar (15%)
        if self.get_avatar_url():
            score += 15
            checklist.append({"key": "avatar", "title": "Profile Photo Added", "done": True, "weight": 15})
        else:
            checklist.append({"key": "avatar", "title": "Upload Profile Photo", "done": False, "weight": 15})

        # 2. Title & Bio (20%)
        has_title = bool(self.title and self.title.strip())
        has_bio = bool(self.bio and len(self.bio.strip()) >= 20)
        title_bio_score = (10 if has_title else 0) + (10 if has_bio else 0)
        score += title_bio_score
        checklist.append({"key": "title_bio", "title": "Professional Title & Detailed Bio", "done": (has_title and has_bio), "weight": 20})

        # 3. Skills (15%)
        skill_count = self.skills.count()
        if skill_count >= 3:
            score += 15
            checklist.append({"key": "skills", "title": "Top Skills Added (3+)", "done": True, "weight": 15})
        else:
            checklist.append({"key": "skills", "title": "Add at least 3 Skills", "done": False, "weight": 15})

        # 4. Hourly Rate & Availability (10%)
        has_rate = self.hourly_rate is not None and self.hourly_rate > 0
        if has_rate:
            score += 10
            checklist.append({"key": "rate", "title": "Hourly Rate & Preferred Hours", "done": True, "weight": 10})
        else:
            checklist.append({"key": "rate", "title": "Set Hourly Rate", "done": False, "weight": 10})

        # 5. Education / Certifications / Portfolio (20%)
        has_portfolio = self.portfolio_items.exists() or (self.portfolio_url and self.portfolio_url.strip())
        has_edu_cert = bool(self.education or self.certifications)
        if has_portfolio or has_edu_cert:
            score += 20
            checklist.append({"key": "credentials", "title": "Portfolio, Education or Certifications", "done": True, "weight": 20})
        else:
            checklist.append({"key": "credentials", "title": "Add Portfolio Project or Education", "done": False, "weight": 20})

        # 6. Verification (20%)
        user_verified = getattr(self.user, 'is_verified', False)
        face_verified = getattr(self.user, 'face_verified', False)
        verif_score = (10 if user_verified else 0) + (10 if face_verified else 0)
        score += verif_score
        checklist.append({"key": "verification", "title": "Email & Facial Anti-Bot Verification", "done": (user_verified and face_verified), "weight": 20})

        return {
            "score": min(score, 100),
            "is_top_rated": score >= 85,
            "checklist": checklist
        }


class CompanyProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="company_profile",
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to="avatars/companies/", blank=True, null=True)
    logo_data = models.TextField(blank=True, default="")
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

    def get_logo_url(self):
        if self.logo_data and self.logo_data.strip():
            return self.logo_data
        if self.logo:
            try:
                return self.logo.url
            except Exception:
                pass
        return None


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