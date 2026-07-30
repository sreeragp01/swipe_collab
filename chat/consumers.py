import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_key   = self.scope['url_route']['kwargs']['room_key']
        self.group_name = f"chat_{self.room_key.replace('-', '')}"

        user = self.scope.get('user')

        if not user or not user.is_authenticated:
            await self.close(code=4001)
            return

        is_member = await self.is_room_member(user, self.room_key)
        if not is_member:
            await self.close(code=4003)
            return

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        await self.send(text_data=json.dumps({
            'type':    'connection_established',
            'message': 'Connected to chat.',
        }))

    async def disconnect(self, close_code):
        user = self.scope.get('user')
        if user and user.is_authenticated:
            await self.channel_layer.group_send(self.group_name, {
                'type':            'typing_indicator',
                'sender_id':       str(user.id),
                'sender_email':    user.email,
                'sender_username': user.username or user.email.split('@')[0],
                'is_typing':       False,
            })
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            return

        event_type = data.get('type', 'message')
        user       = self.scope['user']

        if event_type == 'typing':
            await self.channel_layer.group_send(self.group_name, {
                'type':            'typing_indicator',
                'sender_id':       str(user.id),
                'sender_email':    user.email,
                'sender_username': user.username or user.email.split('@')[0],
                'is_typing':       data.get('is_typing', False),
            })
            return

        if event_type == 'read_receipt':
            message_id = data.get('message_id')
            if message_id:
                await self.mark_message_read(message_id, user)
                await self.channel_layer.group_send(self.group_name, {
                    'type':          'read_receipt_event',
                    'message_id':    message_id,
                    'read_by_id':    str(user.id),
                    'read_by_email': user.email,
                })
            return

        if event_type == 'reaction':
            message_id = data.get('message_id')
            emoji      = data.get('emoji', '')
            if message_id and emoji:
                await self.save_reaction(message_id, user, emoji)
                await self.channel_layer.group_send(self.group_name, {
                    'type':            'reaction_event',
                    'message_id':      message_id,
                    'sender_id':       str(user.id),
                    'sender_email':    user.email,
                    'sender_username': user.username or user.email.split('@')[0],
                    'emoji':           emoji,
                })
            return

        if event_type == 'audio_sent':
            message_data = data.get('message', {})
            await self.channel_layer.group_send(self.group_name, {
                'type':         'broadcast_audio',
                'sender_id':    str(user.id),
                'message_data': message_data,
            })
            return

        if event_type == 'delete_message':
            message_id = data.get('message_id')
            if message_id:
                await self.channel_layer.group_send(self.group_name, {
                    'type':       'message_deleted_event',
                    'message_id': message_id,
                })
            return



        # Default — text message
        content      = data.get('content', '').strip()
        message_type = data.get('message_type', 'text')
        file_url     = data.get('file', None)

        if not content and not file_url:
            return

        try:
            saved = await self.save_message(user, self.room_key, content, message_type, file_url)
        except Exception as e:
            await self.send(text_data=json.dumps({
                'type':   'error',
                'detail': str(e),
            }))
            return

        await self.channel_layer.group_send(self.group_name, {
            'type':            'chat_message',
            'message_id':      saved['id'],
            'sender_id':       str(user.id),
            'sender_email':    user.email,
            'sender_username': user.username or user.email.split('@')[0],
            'content':         content,
            'message_type':    message_type,
            'file':            saved.get('file'),
            'is_read':         False,
            'created_at':      saved['created_at'],
        })

    # ── Group event handlers ───────────────────

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type':            'message',
            'message_id':      event['message_id'],
            'sender_id':       event['sender_id'],
            'sender_email':    event['sender_email'],
            'sender_username': event.get('sender_username', ''),
            'content':         event['content'],
            'message_type':    event['message_type'],
            'file':            event.get('file'),
            'is_read':         event['is_read'],
            'created_at':      event['created_at'],
        }))

    async def broadcast_audio(self, event):
        user = self.scope['user']
        if str(user.id) != event['sender_id']:
            m = event['message_data']
            await self.send(text_data=json.dumps({
                'type':            'message',
                'message_id':      m.get('id'),
                'sender_id':       event['sender_id'],
                'sender_email':    m.get('sender_email', ''),
                'sender_username': m.get('sender_username', ''),
                'content':         m.get('content', '🎤 Voice Note'),
                'message_type':    'audio',
                'file':            m.get('file'),
                'is_read':         False,
                'created_at':      m.get('created_at'),
            }))

    async def message_deleted_event(self, event):
        await self.send(text_data=json.dumps({
            'type':       'message_deleted',
            'message_id': event['message_id'],
        }))




    async def typing_indicator(self, event):
        user = self.scope['user']
        if str(user.id) != event['sender_id']:
            await self.send(text_data=json.dumps({
                'type':            'typing',
                'sender_id':       event['sender_id'],
                'sender_email':    event['sender_email'],
                'sender_username': event.get('sender_username', ''),
                'is_typing':       event['is_typing'],
            }))

    async def read_receipt_event(self, event):
        await self.send(text_data=json.dumps({
            'type':          'read_receipt',
            'message_id':    event['message_id'],
            'read_by_id':    event['read_by_id'],
            'read_by_email': event['read_by_email'],
        }))

    async def reaction_event(self, event):
        await self.send(text_data=json.dumps({
            'type':         'reaction',
            'message_id':   event['message_id'],
            'sender_id':    event['sender_id'],
            'sender_email': event['sender_email'],
            'emoji':        event['emoji'],
        }))

    # ── Database helpers ───────────────────────

    @database_sync_to_async
    def is_room_member(self, user, room_key):
        from chat.models import ChatRoom
        try:
            room = ChatRoom.objects.select_related(
                'match__user1', 'match__user2'
            ).get(room_key=room_key)
            return room.match.user1_id == user.id or room.match.user2_id == user.id
        except ChatRoom.DoesNotExist:
            return False

    @database_sync_to_async
    def save_message(self, user, room_key, content, message_type, file_url=None):
        from chat.models import ChatRoom, Message
        room = ChatRoom.objects.get(room_key=room_key)

        match = room.match
        match.reset_expiry()

        msg = Message.objects.create(
            room         = room,
            sender       = user,
            content      = content,
            message_type = message_type,
            file         = file_url if file_url else None
        )
        return {
            'id':         msg.id,
            'file':       msg.file.url if msg.file else file_url,
            'created_at': str(msg.created_at),
        }


    @database_sync_to_async
    def mark_message_read(self, message_id, user):
        from chat.models import Message
        try:
            msg = Message.objects.get(pk=message_id)
            if msg.sender_id != user.id:
                msg.mark_read()
        except Message.DoesNotExist:
            pass

    @database_sync_to_async
    def save_reaction(self, message_id, user, emoji):
        from chat.models import Message, MessageReaction
        try:
            msg = Message.objects.get(pk=message_id)
            MessageReaction.objects.update_or_create(
                message=msg,
                user=user,
                defaults={'emoji': emoji},
            )
        except Message.DoesNotExist:
            pass