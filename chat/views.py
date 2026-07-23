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
            serializer.save(room=room, sender=request.user)
            try:
                stats = request.user.engagement_stats
                stats.increment('message_count')
            except Exception:
                pass
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)