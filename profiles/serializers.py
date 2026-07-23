from rest_framework import serializers
from .models import Skill, FreelancerProfile, CompanyProfile


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name', 'category']


class FreelancerProfileSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    skill_ids = serializers.PrimaryKeyRelatedField(
        queryset=Skill.objects.all(),
        many=True,
        write_only=True,
        source='skills',
    )
    email = serializers.EmailField(source='user.email', read_only=True)
    role = serializers.CharField(source='user.role', read_only=True)
    is_trial_active = serializers.BooleanField(source='user.is_trial_active', read_only=True)
    trial_ends_at = serializers.DateTimeField(source='user.trial_ends_at', read_only=True)

    class Meta:
        model = FreelancerProfile
        fields = [
            'id', 'email', 'role',
            'name', 'bio', 'avatar',
            'portfolio_url', 'github_url', 'linkedin_url',
            'experience_years', 'availability',
            'city', 'country',
            'skills', 'skill_ids',
            'is_trial_active', 'trial_ends_at',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class FreelancerProfileCardSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    user_id = serializers.UUIDField(source='user.id', read_only=True)
    role = serializers.CharField(source='user.role', read_only=True)

    class Meta:
        model = FreelancerProfile
        fields = [
            'id', 'user_id', 'email', 'role', 'name', 'bio', 'avatar',
            'experience_years', 'availability',
            'city', 'country', 'skills',
        ]


class CompanyProfileSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    skill_ids = serializers.PrimaryKeyRelatedField(
        queryset=Skill.objects.all(),
        many=True,
        write_only=True,
        source='skills',
    )
    email = serializers.EmailField(source='user.email', read_only=True)
    role = serializers.CharField(source='user.role', read_only=True)

    class Meta:
        model = CompanyProfile
        fields = [
            'id', 'email', 'role',
            'name', 'description', 'logo',
            'website_url', 'city', 'country',
            'skills', 'skill_ids',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class CompanyProfileCardSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    user_id = serializers.UUIDField(source='user.id', read_only=True)
    role = serializers.CharField(source='user.role', read_only=True)

    class Meta:
        model = CompanyProfile
        fields = [
            'id', 'user_id', 'email', 'role', 'name', 'description',
            'logo', 'website_url', 'city', 'country', 'skills',
        ]