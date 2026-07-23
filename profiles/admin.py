from django.contrib import admin
from .models import Skill, FreelancerProfile, CompanyProfile


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display  = ['name', 'category']
    list_filter   = ['category']
    search_fields = ['name']
    ordering      = ['category', 'name']


class SkillInline(admin.TabularInline):
    model  = FreelancerProfile.skills.through
    extra  = 0
    verbose_name        = 'Skill'
    verbose_name_plural = 'Skills'


@admin.register(FreelancerProfile)
class FreelancerProfileAdmin(admin.ModelAdmin):
    list_display   = ['name', 'user', 'experience_years', 'availability', 'city', 'country', 'created_at']
    list_filter    = ['availability', 'country']
    search_fields  = ['name', 'user__email', 'city', 'country']
    readonly_fields = ['created_at', 'updated_at']
    filter_horizontal = ['skills']

    fieldsets = (
        ('User',        {'fields': ('user',)}),
        ('Profile',     {'fields': ('name', 'bio', 'avatar')}),
        ('Experience',  {'fields': ('experience_years', 'availability')}),
        ('Location',    {'fields': ('city', 'country')}),
        ('Links',       {'fields': ('portfolio_url', 'github_url', 'linkedin_url')}),
        ('Skills',      {'fields': ('skills',)}),
        ('Timestamps',  {'fields': ('created_at', 'updated_at')}),
    )


@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    list_display   = ['name', 'user', 'city', 'country', 'created_at']
    list_filter    = ['country']
    search_fields  = ['name', 'user__email', 'city']
    readonly_fields = ['created_at', 'updated_at']
    filter_horizontal = ['skills']

    fieldsets = (
        ('User',        {'fields': ('user',)}),
        ('Company',     {'fields': ('name', 'description', 'logo', 'website_url')}),
        ('Location',    {'fields': ('city', 'country')}),
        ('Skills',      {'fields': ('skills',)}),
        ('Timestamps',  {'fields': ('created_at', 'updated_at')}),
    )