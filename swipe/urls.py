from django.urls import path
from .views import SwipeFeedView, SwipeActionView, SwipeFilterView, WhoLikedMeView

urlpatterns = [
    path('feed/',         SwipeFeedView.as_view(),    name='swipe-feed'),
    path('action/',       SwipeActionView.as_view(),  name='swipe-action'),
    path('filter/',       SwipeFilterView.as_view(),  name='swipe-filter'),
    path('who-liked-me/', WhoLikedMeView.as_view(),   name='swipe-who-liked-me'),
]