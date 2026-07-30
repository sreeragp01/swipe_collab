from django.urls import path
from .views import ChatRoomListView, ChatRoomDetailView, MessageListView, MessageDeleteView

urlpatterns = [
    path('rooms/',                          ChatRoomListView.as_view(),   name='chat-room-list'),
    path('rooms/<str:room_key>/',           ChatRoomDetailView.as_view(), name='chat-room-detail'),
    path('rooms/<str:room_key>/messages/',  MessageListView.as_view(),    name='chat-message-list'),
    path('messages/<int:message_id>/delete/', MessageDeleteView.as_view(),  name='chat-message-delete'),
]