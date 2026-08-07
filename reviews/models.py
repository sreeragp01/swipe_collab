from django.conf import settings
from django.db import models


class Review(models.Model):
    project = models.ForeignKey(
        "projects.Project",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviews",
    )
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="given_reviews",
    )
    reviewee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="received_reviews",
    )
    rating_communication = models.PositiveSmallIntegerField(default=5)
    rating_quality = models.PositiveSmallIntegerField(default=5)
    rating_delivery = models.PositiveSmallIntegerField(default=5)
    overall_rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.0)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "reviews_review"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Review by {self.reviewer.email} → {self.reviewee.email} ({self.overall_rating}★)"
