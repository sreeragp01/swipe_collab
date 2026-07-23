from django.contrib import admin
from .models import SwipeAction, SwipeFilter, SkillMatchScore


@admin.register(SwipeAction)
class SwipeActionAdmin(admin.ModelAdmin):
    list_display  = ['swiper', 'target', 'action', 'created_at']
    list_filter   = ['action']
    search_fields = ['swiper__email', 'target__email']
    ordering      = ['-created_at']
    readonly_fields = ['created_at']


@admin.register(SwipeFilter)
class SwipeFilterAdmin(admin.ModelAdmin):
    list_display  = ['user', 'experience_min', 'experience_max', 'country', 'city', 'availability', 'updated_at']
    search_fields = ['user__email', 'country', 'city']
    readonly_fields = ['updated_at']
    filter_horizontal = ['required_skills']


@admin.register(SkillMatchScore)
class SkillMatchScoreAdmin(admin.ModelAdmin):
    list_display  = ['user', 'target', 'score', 'calculated_at']
    search_fields = ['user__email', 'target__email']
    ordering      = ['-score']
    readonly_fields = ['calculated_at']