from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    RegisterView,
    LoginView,
    LogoutView,
    MeView,
    TrialStatusView,
    ChangePasswordView,
    FaceVerifyView,
    VerifyEmailView,
    InstantVerifyEmailView,
    ResendVerificationEmailView,
    PasswordResetRequestView,
    PasswordResetValidateView,
    PasswordResetConfirmView,
)

urlpatterns = [
    path('register/',         RegisterView.as_view(),      name='auth-register'),
    path('login/',            LoginView.as_view(),          name='auth-login'),
    path('logout/',           LogoutView.as_view(),         name='auth-logout'),
    path('token/refresh/',    TokenRefreshView.as_view(),   name='auth-token-refresh'),
    path('me/',               MeView.as_view(),             name='auth-me'),
    path('trial-status/',     TrialStatusView.as_view(),    name='auth-trial-status'),
    path('change-password/',  ChangePasswordView.as_view(), name='auth-change-password'),
    path('face-verify/',      FaceVerifyView.as_view(),     name='auth-face-verify'),
    path('resend-email/',     ResendVerificationEmailView.as_view(), name='auth-resend-email'),
    path('instant-verify/',   InstantVerifyEmailView.as_view(),      name='auth-instant-verify'),
    path('verify-email/<str:token>/', VerifyEmailView.as_view(), name='auth-verify-email'),
    path('password-reset/',   PasswordResetRequestView.as_view(),    name='auth-password-reset'),
    path('password-reset-validate/', PasswordResetValidateView.as_view(), name='auth-password-reset-validate'),
    path('password-reset-confirm/',  PasswordResetConfirmView.as_view(),  name='auth-password-reset-confirm'),
]