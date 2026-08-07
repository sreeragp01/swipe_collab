from django.urls import path
from reviews.views import ReviewListCreateView

urlpatterns = [
    path('', ReviewListCreateView.as_view(), name='review-list-create'),
]
