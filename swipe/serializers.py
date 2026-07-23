from rest_framework import serializers
from .models import SwipeAction, SwipeFilter
from profiles.serializers import SkillSerializer


class SwipeActionSerializer(serializers.ModelSerializer):
    swiper = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = SwipeAction
        fields = ['id', 'swiper', 'target', 'action', 'created_at']
        read_only_fields = ['id', 'swiper', 'created_at']


class SwipeFilterSerializer(serializers.ModelSerializer):
    required_skills = SkillSerializer(many=True, read_only=True)
    skill_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        write_only=True,
        source='required_skills',
        queryset=__import__('profiles.models', fromlist=['Skill']).Skill.objects.all(),
    )

    class Meta:
        model = SwipeFilter
        fields = [
            'id', 'experience_min', 'experience_max',
            'required_skills', 'skill_ids',
            'country', 'city', 'availability', 'updated_at',
        ]
        read_only_fields = ['id', 'updated_at']