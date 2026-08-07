from rest_framework import generics, permissions
from reviews.models import Review
from reviews.serializers import ReviewSerializer


class ReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.query_params.get("user_id")
        if user_id:
            return Review.objects.filter(reviewee_id=user_id)
        return Review.objects.all()

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)
