from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from users.password_reset import (
    generate_password_reset_token,
    verify_password_reset_token,
    send_password_reset_email,
)

User = get_user_model()


class PasswordResetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="developer@swipecollab.com",
            username="swipe_dev",
            password="OriginalPassword@123",
            role=User.ROLE_FREELANCER,
        )

    def test_generate_and_verify_token_valid(self):
        uidb64, token = generate_password_reset_token(self.user)
        self.assertTrue(uidb64)
        self.assertTrue(token)

        verified_user, error = verify_password_reset_token(uidb64, token)
        self.assertIsNone(error)
        self.assertEqual(verified_user, self.user)

    def test_verify_token_invalid_or_tampered(self):
        uidb64, token = generate_password_reset_token(self.user)
        # Tamper token
        tampered_token = token[:-4] + "wxyz"
        user, error = verify_password_reset_token(uidb64, tampered_token)
        self.assertIsNone(user)
        self.assertIn("invalid or has expired", error.lower())

        # Invalid base64 uid
        user, error = verify_password_reset_token("invalid_uid_b64", token)
        self.assertIsNone(user)
        self.assertIn("invalid", error.lower())

    def test_password_reset_request_view_valid_email(self):
        url = reverse('auth-password-reset')
        response = self.client.post(url, {'email': 'developer@swipecollab.com'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data.get('email_sent'))
        self.assertIn('If an account with that email address exists', response.data.get('message'))

    def test_password_reset_request_view_nonexistent_email_anti_enumeration(self):
        url = reverse('auth-password-reset')
        response = self.client.post(url, {'email': 'unknown_user_99@example.com'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data.get('email_sent'))
        self.assertIn('If an account with that email address exists', response.data.get('message'))

    def test_password_reset_validate_view(self):
        uidb64, token = generate_password_reset_token(self.user)
        url = reverse('auth-password-reset-validate')

        # Valid token
        response = self.client.post(url, {'uid': uidb64, 'token': token}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data.get('valid'))
        self.assertIn('@', response.data.get('email'))

        # Invalid token
        response = self.client.post(url, {'uid': uidb64, 'token': 'fake-token'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data.get('valid'))

    def test_password_reset_confirm_successful_flow(self):
        uidb64, token = generate_password_reset_token(self.user)
        url = reverse('auth-password-reset-confirm')

        new_password = "BrandNewSecurePassword@2026!"
        response = self.client.post(url, {
            'uid': uidb64,
            'token': token,
            'new_password': new_password,
            'new_password2': new_password,
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data.get('success'))

        # Verify old password no longer works
        self.user.refresh_from_db()
        self.assertFalse(self.user.check_password("OriginalPassword@123"))

        # Verify new password works
        self.assertTrue(self.user.check_password(new_password))

        # Verify token is single-use and now invalid
        verified_user, error = verify_password_reset_token(uidb64, token)
        self.assertIsNone(verified_user)
        self.assertIsNotNone(error)

        # Verify confirm endpoint rejects reused token
        second_response = self.client.post(url, {
            'uid': uidb64,
            'token': token,
            'new_password': 'AnotherPassword@999',
            'new_password2': 'AnotherPassword@999',
        }, format='json')
        self.assertEqual(second_response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_reset_confirm_password_mismatch(self):
        uidb64, token = generate_password_reset_token(self.user)
        url = reverse('auth-password-reset-confirm')

        response = self.client.post(url, {
            'uid': uidb64,
            'token': token,
            'new_password': 'Password123!',
            'new_password2': 'DifferentPassword123!',
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('new_password', response.data)
