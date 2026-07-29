from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .email_verification import send_verification_email, verify_token
from .face_verification import verify_face_with_opencv
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserSerializer,
    ChangePasswordSerializer,
    FaceVerifySerializer,
)

User = get_user_model()


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            base_url = f"{request.scheme}://{request.get_host()}"
            import threading
            threading.Thread(
                target=send_verification_email,
                args=(user,),
                kwargs={'base_url': base_url},
                daemon=True
            ).start()

            return Response({
                'message': (
                    'Registration successful. 1 month free trial started. '
                    'Please check your email to verify your account.'
                    if user.is_freelancer else
                    'Registration successful. Please check your email to verify your account.'
                ),
                'email_sent': True,
                'user': UserSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            email = request.data.get('email')
            try:
                user = User.objects.get(email=email)
                if user.is_freelancer and user.trial_expired and user.is_trial_active:
                    user.is_trial_active = False
                    user.save(update_fields=['is_trial_active'])
                    response.data['trial_expired'] = True
                    response.data['has_access'] = user.has_access
                    response.data['message'] = 'Your free trial has expired. Please pay ₹49 to continue.'
            except User.DoesNotExist:
                pass
        return response


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            token = RefreshToken(request.data['refresh'])
            token.blacklist()
            return Response({'message': 'Logged out successfully.'})
        except Exception:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)

    def patch(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TrialStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if not user.is_freelancer:
            return Response(
                {'message': 'Trial is only available for freelancers.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        remaining = None
        if user.trial_ends_at and not user.trial_expired:
            delta = user.trial_ends_at - timezone.now()
            remaining = max(delta.days, 0)
        return Response({
            'is_trial_active': user.is_trial_active,
            'trial_started_at': user.trial_started_at,
            'trial_ends_at': user.trial_ends_at,
            'trial_expired': user.trial_expired,
            'days_remaining': remaining,
            'has_access': user.has_access,
        })


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Password changed successfully.'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, token):
        user, error = verify_token(token)
        if error:
            return Response({'detail': error}, status=status.HTTP_400_BAD_REQUEST)

        if user.is_verified:
            return Response({'message': 'Email already verified.', 'is_verified': True})

        user.is_verified = True
        user.save(update_fields=['is_verified'])

        return Response({
            'message': 'Email verified successfully!',
            'is_verified': True,
        })


class InstantVerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if email:
            try:
                user = User.objects.get(email=email.strip().lower())
            except User.DoesNotExist:
                return Response({'detail': 'No account found with that email address.'}, status=status.HTTP_404_NOT_FOUND)
        elif request.user and request.user.is_authenticated:
            user = request.user
        else:
            return Response({'detail': 'Email address or authentication is required.'}, status=status.HTTP_400_BAD_REQUEST)

        user.is_verified = True
        user.save(update_fields=['is_verified'])
        return Response({
            'message': f'Email {user.email} verified successfully!',
            'email': user.email,
            'is_verified': True
        })


class ResendVerificationEmailView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if email:
            try:
                user = User.objects.get(email=email.strip().lower())
            except User.DoesNotExist:
                return Response({'detail': 'No user account found with that email address.'}, status=status.HTTP_404_NOT_FOUND)
        elif request.user and request.user.is_authenticated:
            user = request.user
        else:
            return Response({'detail': 'Email address is required.'}, status=status.HTTP_400_BAD_REQUEST)

        if user.is_verified:
            return Response({'message': f'Email {user.email} is already verified.', 'is_verified': True})

        from .email_verification import generate_verification_token
        token = generate_verification_token(user)
        sent, info = send_verification_email(user, request)

        return Response({
            'message': f'Verification OTP/token dispatched to {user.email}.',
            'email': user.email,
            'token': token,
            'info': info,
            'is_verified': False
        })


class FaceVerifyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = FaceVerifySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        face_image = serializer.validated_data['face_image']

        # Check file type
        if face_image.content_type not in ['image/jpeg', 'image/png', 'image/jpg', 'image/webp']:
            return Response(
                {'detail': 'Only JPEG and PNG images are accepted.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        result = verify_face_with_opencv(face_image)

        if result['verified']:
            request.user.face_verified = True
            request.user.save(update_fields=['face_verified'])
            return Response({
                'message': 'Face verified successfully!',
                'face_verified': True,
                'confidence': result.get('confidence'),
                'details': {
                    'face_count': result.get('face_count'),
                    'eye_count': result.get('eye_count'),
                    'face_size_ratio': result.get('face_size_ratio'),
                }
            })

        return Response({
            'detail': result.get('reason', 'Face verification failed.'),
            'face_verified': False,
            'face_count': result.get('face_count', 0),
        }, status=status.HTTP_400_BAD_REQUEST)