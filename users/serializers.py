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
        validated_data.pop('password2')
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            role=validated_data.get('role', User.ROLE_FREELANCER),
        )
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

    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name',
            'role', 'is_verified', 'face_verified', 'is_paid',
            'is_trial_active', 'trial_started_at', 'trial_ends_at',
            'trial_expired', 'has_access', 'can_swipe',
            'full_name', 'date_joined', 'updated_at',
        ]
        read_only_fields = [
            'id', 'is_verified', 'face_verified', 'is_paid',
            'is_trial_active', 'trial_started_at', 'trial_ends_at',
            'date_joined', 'updated_at',
        ]


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