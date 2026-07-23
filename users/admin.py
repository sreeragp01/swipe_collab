from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display   = ['email', 'username', 'role', 'is_verified', 'face_verified', 'is_paid', 'is_trial_active', 'is_active', 'date_joined']
    list_filter    = ['role', 'is_verified', 'face_verified', 'is_paid', 'is_trial_active', 'is_active', 'is_staff']
    search_fields  = ['email', 'username', 'first_name', 'last_name']
    ordering       = ['-date_joined']
    readonly_fields = ['date_joined', 'updated_at', 'trial_started_at', 'trial_ends_at']

    fieldsets = (
        (None,                  {'fields': ('email', 'username', 'password')}),
        (_('Personal info'),    {'fields': ('first_name', 'last_name')}),
        (_('SwipeCollab'),      {'fields': ('role', 'is_verified', 'face_verified', 'is_paid', 'is_trial_active', 'trial_started_at', 'trial_ends_at')}),
        (_('Permissions'),      {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'),  {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields':  ('email', 'username', 'password1', 'password2', 'role'),
        }),
    )

    actions = ['mark_verified', 'mark_face_verified', 'mark_paid', 'deactivate_users']

    @admin.action(description='Mark selected as email verified')
    def mark_verified(self, request, queryset):
        updated = queryset.update(is_verified=True)
        self.message_user(request, f'{updated} users marked as email verified.')

    @admin.action(description='Mark selected as face verified')
    def mark_face_verified(self, request, queryset):
        updated = queryset.update(face_verified=True)
        self.message_user(request, f'{updated} users marked as face verified.')

    @admin.action(description='Mark selected as paid')
    def mark_paid(self, request, queryset):
        updated = queryset.update(is_paid=True, is_trial_active=False)
        self.message_user(request, f'{updated} users marked as paid.')

    @admin.action(description='Deactivate selected users')
    def deactivate_users(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} users deactivated.')