from django.db.models import Q
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ChatRoom, Message
from .serializers import ChatRoomSerializer, MessageSerializer


class ChatRoomListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        from matches.models import Match
        matches = Match.objects.filter(
            Q(user1=request.user) | Q(user2=request.user)
        )
        for m in matches:
            ChatRoom.objects.get_or_create(match=m)

        rooms = ChatRoom.objects.filter(
            Q(match__user1=request.user) | Q(match__user2=request.user)
        ).select_related('match').prefetch_related('messages')
        serializer = ChatRoomSerializer(rooms, many=True, context={'request': request})
        return Response({'rooms': serializer.data, 'count': rooms.count()})


class ChatRoomDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, room_key):
        try:
            room = ChatRoom.objects.get(
                room_key=room_key,
            )
            if room.match.user1 != request.user and room.match.user2 != request.user:
                return Response({'detail': 'Forbidden.'}, status=status.HTTP_403_FORBIDDEN)
            serializer = ChatRoomSerializer(room, context={'request': request})
            return Response(serializer.data)
        except ChatRoom.DoesNotExist:
            return Response({'detail': 'Room not found.'}, status=status.HTTP_404_NOT_FOUND)


class MessageListView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get(self, request, room_key):
        try:
            room = ChatRoom.objects.get(room_key=room_key)
            if room.match.user1 != request.user and room.match.user2 != request.user:
                return Response({'detail': 'Forbidden.'}, status=status.HTTP_403_FORBIDDEN)
        except ChatRoom.DoesNotExist:
            return Response({'detail': 'Room not found.'}, status=status.HTTP_404_NOT_FOUND)

        room.messages.exclude(sender=request.user).update(is_read=True)
        messages = room.messages.all()
        serializer = MessageSerializer(messages, many=True)
        return Response({'messages': serializer.data, 'count': messages.count()})

    def post(self, request, room_key):
        try:
            room = ChatRoom.objects.get(room_key=room_key)
            if room.match.user1 != request.user and room.match.user2 != request.user:
                return Response({'detail': 'Forbidden.'}, status=status.HTTP_403_FORBIDDEN)
        except ChatRoom.DoesNotExist:
            return Response({'detail': 'Room not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            msg_obj = serializer.save(room=room, sender=request.user)
            recipient = room.match.user2 if room.match.user1 == request.user else room.match.user1
            try:
                from notifications.models import notify_user, Notification
                notify_user(
                    user=recipient,
                    sender=request.user,
                    notification_type=Notification.TYPE_CHAT_MESSAGE,
                    title="New Chat Message 💬",
                    message=f"{request.user.full_name}: {msg_obj.text[:50] if hasattr(msg_obj, 'text') and msg_obj.text else 'Sent a message'}",
                    link=f"/chat/?match={room.match.id}",
                )
            except Exception as e:
                print(f"Chat notification error: {e}")

            try:
                stats = request.user.engagement_stats
                stats.increment('message_count')
            except Exception:
                pass
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessageDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, message_id):
        try:
            msg = Message.objects.get(id=message_id)
            if msg.sender != request.user:
                return Response({'detail': 'You can only delete your own messages.'}, status=status.HTTP_403_FORBIDDEN)
            
            msg.is_deleted = True
            msg.content = "🚫 This message was deleted"
            if msg.file:
                try:
                    msg.file.delete(save=False)
                except Exception:
                    pass
                msg.file = None
            msg.save(update_fields=['is_deleted', 'content', 'file'])
            return Response({'message': 'Message deleted successfully.', 'id': msg.id})
        except Message.DoesNotExist:
            return Response({'detail': 'Message not found.'}, status=status.HTTP_404_NOT_FOUND)