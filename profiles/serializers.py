from rest_framework import serializers
from .models import Skill, FreelancerProfile, CompanyProfile, PortfolioItem, PortfolioItemLike, PortfolioItemComment


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name', 'category']


class PortfolioItemCommentSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    user_avatar = serializers.SerializerMethodField()

    class Meta:
        model = PortfolioItemComment
        fields = ['id', 'user', 'user_name', 'user_avatar', 'text', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']

    def get_user_name(self, obj):
        if hasattr(obj.user, 'freelancer_profile'):
            return obj.user.freelancer_profile.name
        if hasattr(obj.user, 'company_profile'):
            return obj.user.company_profile.name
        return obj.user.email

    def get_user_avatar(self, obj):
        if hasattr(obj.user, 'freelancer_profile') and obj.user.freelancer_profile.avatar:
            return obj.user.freelancer_profile.avatar.url
        if hasattr(obj.user, 'company_profile') and obj.user.company_profile.logo:
            return obj.user.company_profile.logo.url
        return None


class PortfolioItemSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    is_liked_by_me = serializers.SerializerMethodField()
    comments = PortfolioItemCommentSerializer(many=True, read_only=True)

    class Meta:
        model = PortfolioItem
        fields = [
            'id', 'title', 'description', 'experience_gained',
            'media_file', 'project_url', 'created_at',
            'like_count', 'comment_count', 'is_liked_by_me', 'comments',
        ]
        read_only_fields = ['id', 'created_at']

    def get_like_count(self, obj):
        return obj.likes.count()

    def get_comment_count(self, obj):
        return obj.comments.count()

    def get_is_liked_by_me(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False


class FreelancerProfileSerializer(serializers.ModelSerializer):
    portfolio_url = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    github_url = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    linkedin_url = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    skills = SkillSerializer(many=True, read_only=True)
    skill_ids = serializers.PrimaryKeyRelatedField(
        queryset=Skill.objects.all(),
        many=True,
        write_only=True,
        source='skills',
        required=False,
    )
    portfolio_items = PortfolioItemSerializer(many=True, read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    role = serializers.CharField(source='user.role', read_only=True)
    is_trial_active = serializers.BooleanField(source='user.is_trial_active', read_only=True)
    trial_ends_at = serializers.DateTimeField(source='user.trial_ends_at', read_only=True)

    class Meta:
        model = FreelancerProfile
        fields = [
            'id', 'email', 'role',
            'name', 'bio', 'avatar',
            'portfolio_url', 'portfolio_style', 'portfolio_custom_data',
            'github_url', 'linkedin_url',
            'experience_years', 'availability',
            'city', 'country',
            'skills', 'skill_ids', 'portfolio_items',
            'is_trial_active', 'trial_ends_at',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class FreelancerProfileCardSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    portfolio_items = PortfolioItemSerializer(many=True, read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    user_id = serializers.UUIDField(source='user.id', read_only=True)
    role = serializers.CharField(source='user.role', read_only=True)

    class Meta:
        model = FreelancerProfile
        fields = [
            'id', 'user_id', 'email', 'role', 'name', 'bio', 'avatar',
            'portfolio_url', 'portfolio_style', 'portfolio_custom_data',
            'github_url', 'linkedin_url',
            'experience_years', 'availability',
            'city', 'country', 'skills', 'portfolio_items',
        ]


class CompanyProjectCardSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    description = serializers.CharField()
    duration = serializers.CharField()
    status = serializers.CharField()
    budget_min = serializers.DecimalField(max_digits=10, decimal_places=2)
    budget_max = serializers.DecimalField(max_digits=10, decimal_places=2)
    deadline = serializers.DateField(required=False, allow_null=True)
    skills = SkillSerializer(many=True, read_only=True)


class CompanyProfileSerializer(serializers.ModelSerializer):
    website_url = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    skills = SkillSerializer(many=True, read_only=True)
    skill_ids = serializers.PrimaryKeyRelatedField(
        queryset=Skill.objects.all(),
        many=True,
        write_only=True,
        source='skills',
        required=False,
    )
    email = serializers.EmailField(source='user.email', read_only=True)
    role = serializers.CharField(source='user.role', read_only=True)
    open_projects = serializers.SerializerMethodField()

    class Meta:
        model = CompanyProfile
        fields = [
            'id', 'email', 'role',
            'name', 'description', 'logo',
            'website_url', 'city', 'country',
            'skills', 'skill_ids', 'open_projects',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_open_projects(self, obj):
        projects = obj.projects.filter(status='open')
        return CompanyProjectCardSerializer(projects, many=True).data


class CompanyProfileCardSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    user_id = serializers.UUIDField(source='user.id', read_only=True)
    role = serializers.CharField(source='user.role', read_only=True)
    open_projects = serializers.SerializerMethodField()

    class Meta:
        model = CompanyProfile
        fields = [
            'id', 'user_id', 'email', 'role', 'name', 'description',
            'logo', 'website_url', 'city', 'country', 'skills', 'open_projects',
        ]

    def get_open_projects(self, obj):
        projects = obj.projects.filter(status='open')
        return CompanyProjectCardSerializer(projects, many=True).data