from django.contrib import admin
from .models import ProfileView, EngagementStat


@admin.register(ProfileView)
class ProfileViewAdmin(admin.ModelAdmin):
    list_display   = ['id', 'viewer', 'viewed_profile', 'source', 'viewed_at']
    list_filter    = ['source']
    search_fields  = ['viewer__email', 'viewed_profile__email']
    ordering       = ['-viewed_at']
    readonly_fields = ['viewed_at']


@admin.register(EngagementStat)
class EngagementStatAdmin(admin.ModelAdmin):
    list_display   = [
        'user', 'total_swipes_made', 'total_likes_received',
        'match_count', 'message_count', 'profile_view_count',
        'projects_posted', 'applications_received', 'applications_sent',
        'updated_at',
    ]
    search_fields  = ['user__email']
    ordering       = ['-match_count']
    readonly_fields = ['updated_at']

    actions = ['sync_stats']

    @admin.action(description='Re-sync stats from database for selected users')
    def sync_stats(self, request, queryset):
        from analytics.views import sync_stats_for_user
        count = 0
        for stat in queryset:
            sync_stats_for_user(stat.user, stat)
            count += 1
        self.message_user(request, f'{count} user stats synced from database.')