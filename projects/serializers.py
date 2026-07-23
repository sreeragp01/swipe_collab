from rest_framework import serializers
from .models import Project, Application
from profiles.serializers import SkillSerializer, CompanyProfileCardSerializer, FreelancerProfileCardSerializer


class ProjectSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    skill_ids = serializers.PrimaryKeyRelatedField(
        many=True, write_only=True, source='skills',
        queryset=__import__('profiles.models', fromlist=['Skill']).Skill.objects.all(),
    )
    company_name = serializers.CharField(source='company.name', read_only=True)
    application_count = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id', 'company_name', 'title', 'description',
            'duration', 'status', 'budget_min', 'budget_max',
            'skills', 'skill_ids', 'deadline',
            'application_count', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_application_count(self, obj):
        return obj.applications.count()


class ApplicationSerializer(serializers.ModelSerializer):
    freelancer = FreelancerProfileCardSerializer(read_only=True)
    project_title = serializers.CharField(source='project.title', read_only=True)

    class Meta:
        model = Application
        fields = [
            'id', 'project', 'project_title', 'freelancer',
            'cover_letter', 'proposed_rate', 'status',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'freelancer', 'status', 'created_at', 'updated_at']


class CreateApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['cover_letter', 'proposed_rate']