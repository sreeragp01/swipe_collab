from rest_framework.permissions import BasePermission
from django.conf import settings


# ── Set this to True while testing, False in production ──
TESTING_MODE = getattr(settings, 'TESTING_MODE', False)


class IsAllowedToSwipe(BasePermission):
    """
    Allows swipe access if:
    - TESTING_MODE is True (bypass everything), OR
    - User is verified + face verified + (paid or trial active)
    """
    message = 'You must be verified and have an active plan to swipe.'

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if TESTING_MODE:
            return True
        return request.user.can_swipe


class IsPaidUser(BasePermission):
    """
    Allows access if:
    - TESTING_MODE is True, OR
    - User has paid
    """
    message = 'This feature requires a paid plan.'

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if TESTING_MODE:
            return True
        return request.user.is_paid


class IsVerified(BasePermission):
    """
    Allows access if:
    - TESTING_MODE is True, OR
    - User email is verified
    """
    message = 'Please verify your email first.'

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if TESTING_MODE:
            return True
        return request.user.is_verified