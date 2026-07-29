from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password2', 'role']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': 'Passwords do not match.'})
        return attrs

    def create(self, validated_data):
        from django.conf import settings
        validated_data.pop('password2')
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            role=validated_data.get('role', User.ROLE_FREELANCER),
        )
        if getattr(settings, 'DEBUG', False):
            user.is_verified = True
            user.face_verified = True
            user.is_paid = True
            user.save(update_fields=['is_verified', 'face_verified', 'is_paid'])
        if user.is_freelancer:
            user.start_trial()
        return user


class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['id'] = str(self.user.id)
        data['email'] = self.user.email
        data['role'] = self.user.role
        data['is_verified'] = self.user.is_verified
        data['face_verified'] = self.user.face_verified
        data['is_paid'] = self.user.is_paid
        data['is_trial_active'] = self.user.is_trial_active
        data['trial_ends_at'] = str(self.user.trial_ends_at) if self.user.trial_ends_at else None
        data['trial_expired'] = self.user.trial_expired
        data['has_access'] = self.user.has_access
        return data


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    can_swipe = serializers.ReadOnlyField()
    has_access = serializers.ReadOnlyField()
    trial_expired = serializers.ReadOnlyField()
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name',
            'role', 'avatar', 'is_verified', 'face_verified', 'is_paid',
            'is_trial_active', 'trial_started_at', 'trial_ends_at',
            'trial_expired', 'has_access', 'can_swipe',
            'full_name', 'date_joined', 'updated_at',
        ]
        read_only_fields = [
            'id', 'is_verified', 'face_verified', 'is_paid',
            'is_trial_active', 'trial_started_at', 'trial_ends_at',
            'date_joined', 'updated_at',
        ]

    def get_avatar(self, obj):
        request = self.context.get('request')
        url = None
        if hasattr(obj, 'freelancer_profile') and obj.freelancer_profile.avatar:
            url = obj.freelancer_profile.avatar.url
        elif hasattr(obj, 'company_profile') and obj.company_profile.logo:
            url = obj.company_profile.logo.url
        if url and request:
            return request.build_absolute_uri(url)
        return url


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
    new_password2 = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({'new_password': 'Passwords do not match.'})
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Old password is incorrect.')
        return value

    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class FaceVerifySerializer(serializers.Serializer):
    face_image = serializers.ImageField()