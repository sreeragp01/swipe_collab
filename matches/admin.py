from django.contrib import admin
from .models import Match, CollaborationSession, CollaborationRating


class CollaborationSessionInline(admin.TabularInline):
    model   = CollaborationSession
    extra   = 0
    fields  = ['platform', 'meeting_link', 'status', 'scheduled_at']
    readonly_fields = ['created_at']


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display   = ['id', 'user1', 'user2', 'is_expired', 'hours_remaining_display', 'created_at']
    list_filter    = ['is_expired']
    search_fields  = ['user1__email', 'user2__email']
    ordering       = ['-created_at']
    readonly_fields = ['created_at', 'expires_at']
    inlines        = [CollaborationSessionInline]

    @admin.display(description='Hours remaining')
    def hours_remaining_display(self, obj):
        return f'{obj.hours_remaining}h'


@admin.register(CollaborationSession)
class CollaborationSessionAdmin(admin.ModelAdmin):
    list_display   = ['id', 'match', 'initiated_by', 'platform', 'status', 'scheduled_at', 'created_at']
    list_filter    = ['platform', 'status']
    search_fields  = ['match__user1__email', 'match__user2__email', 'initiated_by__email']
    ordering       = ['-created_at']
    readonly_fields = ['created_at']


@admin.register(CollaborationRating)
class CollaborationRatingAdmin(admin.ModelAdmin):
    list_display   = ['id', 'rated_by', 'rated_user', 'score', 'created_at']
    list_filter    = ['score']
    search_fields  = ['rated_by__email', 'rated_user__email']
    ordering       = ['-created_at']
    readonly_fields = ['created_at']