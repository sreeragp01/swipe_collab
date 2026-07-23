from django.contrib import admin
from .models import ChatRoom, Message, MessageReaction


class MessageInline(admin.TabularInline):
    model        = Message
    extra        = 0
    fields       = ['sender', 'message_type', 'content', 'is_read', 'created_at']
    readonly_fields = ['sender', 'message_type', 'content', 'is_read', 'created_at']
    can_delete   = False
    max_num      = 20


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display   = ['id', 'match', 'room_key', 'message_count', 'created_at']
    search_fields  = ['match__user1__email', 'match__user2__email', 'room_key']
    readonly_fields = ['room_key', 'created_at']
    inlines        = [MessageInline]

    @admin.display(description='Messages')
    def message_count(self, obj):
        return obj.messages.count()


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display   = ['id', 'sender', 'room', 'message_type', 'is_read', 'created_at']
    list_filter    = ['message_type', 'is_read']
    search_fields  = ['sender__email', 'content']
    ordering       = ['-created_at']
    readonly_fields = ['created_at', 'read_at']


@admin.register(MessageReaction)
class MessageReactionAdmin(admin.ModelAdmin):
    list_display   = ['id', 'user', 'message', 'emoji', 'created_at']
    search_fields  = ['user__email', 'emoji']
    readonly_fields = ['created_at']