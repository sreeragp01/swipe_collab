from django.contrib import admin
from .models import Project, Application


class ApplicationInline(admin.TabularInline):
    model        = Application
    extra        = 0
    fields       = ['freelancer', 'proposed_rate', 'status', 'created_at']
    readonly_fields = ['freelancer', 'proposed_rate', 'created_at']
    can_delete   = False


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display   = ['title', 'company', 'status', 'budget_min', 'budget_max', 'duration', 'application_count', 'created_at']
    list_filter    = ['status', 'duration']
    search_fields  = ['title', 'company__name', 'company__user__email']
    ordering       = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
    filter_horizontal = ['skills']
    inlines        = [ApplicationInline]

    actions = ['mark_open', 'mark_closed']

    @admin.display(description='Applications')
    def application_count(self, obj):
        return obj.applications.count()

    @admin.action(description='Mark selected projects as Open')
    def mark_open(self, request, queryset):
        updated = queryset.update(status=Project.STATUS_OPEN)
        self.message_user(request, f'{updated} projects marked as open.')

    @admin.action(description='Mark selected projects as Cancelled')
    def mark_closed(self, request, queryset):
        updated = queryset.update(status=Project.STATUS_CANCELLED)
        self.message_user(request, f'{updated} projects cancelled.')


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display   = ['id', 'freelancer', 'project', 'proposed_rate', 'status', 'created_at']
    list_filter    = ['status']
    search_fields  = ['freelancer__user__email', 'project__title']
    ordering       = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']

    actions = ['shortlist', 'accept', 'reject']

    @admin.action(description='Shortlist selected applications')
    def shortlist(self, request, queryset):
        updated = queryset.update(status=Application.STATUS_SHORTLISTED)
        self.message_user(request, f'{updated} applications shortlisted.')

    @admin.action(description='Accept selected applications')
    def accept(self, request, queryset):
        updated = queryset.update(status=Application.STATUS_ACCEPTED)
        self.message_user(request, f'{updated} applications accepted.')

    @admin.action(description='Reject selected applications')
    def reject(self, request, queryset):
        updated = queryset.update(status=Application.STATUS_REJECTED)
        self.message_user(request, f'{updated} applications rejected.')