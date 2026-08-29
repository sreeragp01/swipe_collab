import logging
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

logger = logging.getLogger(__name__)
User = get_user_model()


def generate_password_reset_token(user):
    """
    Generates a secure (uidb64, token) pair for a user.
    Uses Django's PasswordResetTokenGenerator which automatically invalidates
    once the user's password changes or upon expiration.
    """
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    return uidb64, token


def verify_password_reset_token(uidb64, token):
    """
    Decodes the user ID and verifies the token.
    Returns (user, None) if valid, or (None, error_message) if invalid/expired.
    """
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return None, "Invalid password reset link."

    if not default_token_generator.check_token(user, token):
        return None, "This password reset link is invalid or has expired."

    if not user.is_active:
        return None, "This account is inactive. Please contact support."

    return user, None


def send_password_reset_email(user, request=None, base_url=None):
    """
    Generates a reset token and sends a branded transactional email.
    Falls back gracefully if SMTP is not configured in development.
    """
    uidb64, token = generate_password_reset_token(user)

    if not base_url:
        if request:
            base_url = f"{request.scheme}://{request.get_host()}"
        else:
            base_url = getattr(settings, 'SITE_URL', 'http://127.0.0.1:8000')

    reset_url = f"{base_url}/reset-password/?uid={uidb64}&token={token}"
    username = user.full_name or user.email.split('@')[0]

    subject = "Reset your SwipeCollab password"

    plain_message = f"""
Hi {username},

We received a request to reset your password for your SwipeCollab account.

Click the link below to set a new password:
{reset_url}

This link is single-use and will expire shortly.

If you did not request a password reset, you can safely ignore this email. Your password will not change and your account remains secure.

— The SwipeCollab Team
https://swipecollab.com
    """.strip()

    html_message = f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Reset your SwipeCollab password</title>
</head>
<body style="margin:0;padding:0;background:#0a0f1e;font-family:'Segoe UI',Roboto,Helvetica,Arial,sans-serif;-webkit-font-smoothing:antialiased;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#0a0f1e;padding:40px 20px;">
    <tr>
      <td align="center">
        <table width="540" cellpadding="0" cellspacing="0"
               style="background:#111827;border:1px solid #1f2937;border-radius:16px;overflow:hidden;box-shadow:0 20px 40px rgba(0,0,0,0.5);">

          <!-- Header -->
          <tr>
            <td style="background:linear-gradient(135deg, #0f172a 0%, #108a00 100%);padding:32px 36px;">
              <table width="100%" cellpadding="0" cellspacing="0">
                <tr>
                  <td>
                    <h1 style="margin:0;color:#ffffff;font-size:1.6rem;font-weight:800;letter-spacing:-0.03em;">
                      Swipe<span style="color:#4ade80;">Collab</span>
                    </h1>
                    <p style="margin:6px 0 0;color:rgba(255,255,255,0.85);font-size:0.875rem;">
                      Account Security Notification
                    </p>
                  </td>
                  <td align="right" style="font-size:2rem;">
                    🔐
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Body -->
          <tr>
            <td style="padding:36px;">
              <h2 style="color:#f9fafb;font-size:1.25rem;font-weight:700;margin:0 0 16px;letter-spacing:-0.01em;">
                Reset your password
              </h2>
              <p style="color:#9ca3af;font-size:0.95rem;line-height:1.6;margin:0 0 20px;">
                Hello <strong style="color:#f3f4f6;">{username}</strong>,
              </p>
              <p style="color:#9ca3af;font-size:0.95rem;line-height:1.6;margin:0 0 28px;">
                We received a request to reset the password for your SwipeCollab account associated with <span style="color:#4ade80;word-break:break-all;">{user.email}</span>. Click the button below to choose a new password.
              </p>

              <!-- CTA Button -->
              <table cellpadding="0" cellspacing="0" style="margin:0 0 32px;" width="100%">
                <tr>
                  <td align="center">
                    <a href="{reset_url}"
                       style="display:inline-block;padding:15px 36px;background:#108a00;background:linear-gradient(135deg,#108a00,#0d7400);
                              color:#ffffff;font-weight:700;font-size:1rem;text-decoration:none;border-radius:10px;
                              box-shadow:0 4px 14px rgba(16,138,0,0.4);letter-spacing:0.02em;">
                      Reset My Password →
                    </a>
                  </td>
                </tr>
              </table>

              <div style="background:#1f2937;border:1px solid #374151;border-radius:8px;padding:16px;margin-bottom:24px;">
                <p style="color:#d1d5db;font-size:0.82rem;line-height:1.5;margin:0;">
                  ⚠️ <strong>Security Notice:</strong> This link is single-use and will automatically expire. If you did not request this password reset, please ignore this email or change your password if you suspect unauthorized access.
                </p>
              </div>

              <p style="color:#6b7280;font-size:0.8rem;line-height:1.5;margin:0;">
                If the button above does not work, copy and paste this link into your browser:<br>
                <a href="{reset_url}" style="color:#4ade80;word-break:break-all;">{reset_url}</a>
              </p>
            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td style="background:#0b0f19;padding:24px 36px;border-top:1px solid #1f2937;text-align:center;">
              <p style="color:#6b7280;font-size:0.78rem;margin:0 0 6px;line-height:1.4;">
                This email was sent automatically by SwipeCollab Security.
              </p>
              <p style="color:#4b5563;font-size:0.75rem;margin:0;">
                © 2026 SwipeCollab. All rights reserved.
              </p>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>
    """.strip()

    has_credentials = bool(getattr(settings, 'EMAIL_HOST_USER', None) and getattr(settings, 'EMAIL_HOST_PASSWORD', None))

    print("==================================================")
    print(f"PASSWORD RESET REQUEST: {user.email}")
    print(f"Reset Link: {reset_url}")
    print(f"UID: {uidb64} | Token: {token}")
    print("==================================================")

    if not has_credentials:
        info_msg = "SMTP Credentials not set in environment. Link printed to server logs."
        return False, reset_url

    import threading

    def _async_send():
        try:
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                html_message=html_message,
                fail_silently=False,
            )
            print(f"Password reset email delivered successfully to {user.email} via SMTP.")
        except Exception as e:
            err_msg = f"SMTP error sending password reset email to {user.email}: {str(e)}"
            logger.error(err_msg)
            print("==================================================")
            print(f"{err_msg}")
            print(f"Fallback Reset Link: {reset_url}")
            print("==================================================")

    thread = threading.Thread(target=_async_send, daemon=True)
    thread.start()

    return True, "Email dispatch initiated in background."
