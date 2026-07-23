from django.urls import path
from .views import (
    MatchListView, MatchDetailView,
    CollaborationSessionListView, CollaborationSessionDetailView,
    CollaborationRatingView, UserRatingsView,
)

urlpatterns = [
    path('',                                                    MatchListView.as_view(),                  name='match-list'),
    path('<int:pk>/',                                           MatchDetailView.as_view(),                name='match-detail'),
    path('<int:match_id>/sessions/',                            CollaborationSessionListView.as_view(),   name='collab-session-list'),
    path('<int:match_id>/sessions/<int:session_id>/',           CollaborationSessionDetailView.as_view(), name='collab-session-detail'),
    path('<int:match_id>/sessions/<int:session_id>/rate/',      CollaborationRatingView.as_view(),        name='collab-rating'),
    path('my-ratings/',                                         UserRatingsView.as_view(),                name='user-ratings'),
]