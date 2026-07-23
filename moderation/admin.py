from django.contrib import admin
from .models import Report, BlockList, UserStrike


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display   = ['id', 'reporter', 'reported_user', 'category', 'status', 'reviewed_by', 'created_at']
    list_filter    = ['status', 'category']
    search_fields  = ['reporter__email', 'reported_user__email', 'reason']
    ordering       = ['-created_at']
    readonly_fields = ['reporter', 'reported_user', 'created_at', 'updated_at']

    fieldsets = (
        ('Report',   {'fields': ('reporter', 'reported_user', 'category', 'reason', 'evidence_url')}),
        ('Review',   {'fields': ('status', 'reviewed_by')}),
        ('Timestamps',{'fields': ('created_at', 'updated_at')}),
    )

    actions = ['mark_reviewed', 'dismiss', 'action_and_strike']

    @admin.action(description='Mark selected reports as Reviewed')
    def mark_reviewed(self, request, queryset):
        updated = queryset.update(status=Report.STATUS_REVIEWED, reviewed_by=request.user)
        self.message_user(request, f'{updated} reports marked as reviewed.')

    @admin.action(description='Dismiss selected reports')
    def dismiss(self, request, queryset):
        updated = queryset.update(status=Report.STATUS_DISMISSED, reviewed_by=request.user)
        self.message_user(request, f'{updated} reports dismissed.')

    @admin.action(description='Action reports + issue strike to reported users')
    def action_and_strike(self, request, queryset):
        count = 0
        for report in queryset:
            report.status      = Report.STATUS_ACTIONED
            report.reviewed_by = request.user
            report.save()
            strike, _ = UserStrike.objects.get_or_create(user=report.reported_user)
            strike.add_strike()
            count += 1
        self.message_user(request, f'{count} reports actioned and strikes issued.')


@admin.register(BlockList)
class BlockListAdmin(admin.ModelAdmin):
    list_display   = ['id', 'blocker', 'blocked', 'reason', 'created_at']
    search_fields  = ['blocker__email', 'blocked__email']
    ordering       = ['-created_at']
    readonly_fields = ['created_at']


@admin.register(UserStrike)
class UserStrikeAdmin(admin.ModelAdmin):
    list_display   = ['user', 'strike_count', 'is_temp_banned', 'temp_ban_until', 'updated_at']
    list_filter    = ['is_temp_banned', 'strike_count']
    search_fields  = ['user__email']
    readonly_fields = ['updated_at']

    actions = ['reset_strikes', 'issue_strike']

    @admin.action(description='Reset strikes to 0 for selected users')
    def reset_strikes(self, request, queryset):
        updated = queryset.update(strike_count=0, is_temp_banned=False, temp_ban_until=None)
        self.message_user(request, f'{updated} users strikes reset.')

    @admin.action(description='Issue one strike to selected users')
    def issue_strike(self, request, queryset):
        for strike in queryset:
            strike.add_strike()
        self.message_user(request, f'{queryset.count()} strikes issued.')