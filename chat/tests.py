from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory
from matches.models import Match
from chat.models import ChatRoom, Message
from chat.serializers import ChatRoomSerializer, MessageSerializer

User = get_user_model()


class ChatSerializerTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(email="alice@example.com", username="alice_dev", password="password123")
        self.user2 = User.objects.create_user(email="bob@example.com", username="bob_designer", password="password123")
        self.match = Match.create(self.user1, self.user2)
        self.room = ChatRoom.objects.create(match=self.match)
        self.factory = APIRequestFactory()

    def test_chatroom_serializer_other_user(self):
        request = self.factory.get('/')
        request.user = self.user1
        serializer = ChatRoomSerializer(self.room, context={'request': request})
        data = serializer.data

        self.assertIn('other_user', data)
        self.assertIsNotNone(data['other_user'])
        self.assertEqual(data['other_user']['username'], 'bob_designer')
        self.assertEqual(data['other_user']['display_name'], 'bob_designer')

    def test_message_serializer_sender_username(self):
        msg = Message.objects.create(room=self.room, sender=self.user1, content="Hello Bob!")
        serializer = MessageSerializer(msg)
        self.assertEqual(serializer.data['sender_username'], 'alice_dev')

