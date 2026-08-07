from rest_framework import serializers
from reviews.models import Review
from users.serializers import UserPublicSerializer


class ReviewSerializer(serializers.ModelSerializer):
    reviewer_detail = UserPublicSerializer(source="reviewer", read_only=True)
    reviewee_detail = UserPublicSerializer(source="reviewee", read_only=True)

    class Meta:
        model = Review
        fields = [
            "id",
            "project",
            "reviewer",
            "reviewer_detail",
            "reviewee",
            "reviewee_detail",
            "rating_communication",
            "rating_quality",
            "rating_delivery",
            "overall_rating",
            "comment",
            "created_at",
        ]
        read_only_fields = ["reviewer", "created_at"]
