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
    path('verify-email/<str:token>/', VerifyEmailView.as_view(), name='auth-verify-email'),
]