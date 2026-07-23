from django.urls import path
from .views import ChatRoomListView, ChatRoomDetailView, MessageListView

urlpatterns = [
    path('rooms/',                          ChatRoomListView.as_view(),   name='chat-room-list'),
    path('rooms/<str:room_key>/',           ChatRoomDetailView.as_view(), name='chat-room-detail'),
    path('rooms/<str:room_key>/messages/',  MessageListView.as_view(),    name='chat-message-list'),
]