from rest_framework import serializers
from .models import Project, Application
from profiles.serializers import SkillSerializer, CompanyProfileCardSerializer, FreelancerProfileCardSerializer


class ProjectSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    skill_ids = serializers.PrimaryKeyRelatedField(
        many=True, write_only=True, source='skills', required=False,
        queryset=__import__('profiles.models', fromlist=['Skill']).Skill.objects.all(),
    )
    skill_names = serializers.ListField(
        child=serializers.CharField(), write_only=True, required=False
    )
    company_name = serializers.CharField(source='company.name', read_only=True)
    application_count = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id', 'company_name', 'title', 'description',
            'duration', 'status', 'budget_min', 'budget_max',
            'skills', 'skill_ids', 'skill_names', 'deadline',
            'application_count', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_application_count(self, obj):
        return obj.applications.count()

    def create(self, validated_data):
        skill_names = validated_data.pop('skill_names', None)
        project = super().create(validated_data)
        if skill_names:
            from profiles.models import Skill
            skills = []
            for name in skill_names:
                name_clean = name.strip()
                if name_clean:
                    skill, _ = Skill.objects.get_or_create(
                        name__iexact=name_clean,
                        defaults={'name': name_clean}
                    )
                    skills.append(skill)
            if skills:
                project.skills.add(*skills)
        return project

    def update(self, instance, validated_data):
        skill_names = validated_data.pop('skill_names', None)
        project = super().update(instance, validated_data)
        if skill_names is not None:
            from profiles.models import Skill
            skills = []
            for name in skill_names:
                name_clean = name.strip()
                if name_clean:
                    skill, _ = Skill.objects.get_or_create(
                        name__iexact=name_clean,
                        defaults={'name': name_clean}
                    )
                    skills.append(skill)
            project.skills.set(skills)
        return project


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