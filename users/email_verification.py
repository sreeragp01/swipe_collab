import hashlib
import hmac
import time
import base64
from django.conf import settings
from django.core.mail import send_mail


def generate_verification_token(user):
    timestamp = str(int(time.time()))
    secret = settings.SECRET_KEY.encode()
    msg = f"{user.id}:{user.email}:{timestamp}".encode()
    signature = hmac.new(secret, msg, hashlib.sha256).hexdigest()
    token = f"{user.id}:{timestamp}:{signature}"
    return base64.urlsafe_b64encode(token.encode()).decode()


def verify_token(token, max_age_seconds=86400):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    try:
        decoded = base64.urlsafe_b64decode(token.encode()).decode()
        parts = decoded.split(":")
        if len(parts) != 3:
            return None, "Invalid token format."
        user_id, timestamp, signature = parts
        if int(time.time()) - int(timestamp) > max_age_seconds:
            return None, "Token expired. Please request a new verification email."
        user = User.objects.get(id=user_id)
        secret = settings.SECRET_KEY.encode()
        msg = f"{user.id}:{user.email}:{timestamp}".encode()
        expected = hmac.new(secret, msg, hashlib.sha256).hexdigest()
        if not hmac.compare_digest(expected, signature):
            return None, "Invalid token."
        return user, None
    except User.DoesNotExist:
        return None, "User not found."
    except Exception as e:
        return None, f"Token error: {str(e)}"


def send_verification_email(user, request=None, base_url=None):
    token = generate_verification_token(user)

    if not base_url:
        if request:
            base_url = f"{request.scheme}://{request.get_host()}"
        else:
            base_url = getattr(settings, 'SITE_URL', 'http://127.0.0.1:8000')

    verify_url = f"{base_url}/verify-email/?token={token}"
    username = user.email.split('@')[0]

    subject = "Verify your SwipeCollab email address"

    plain_message = f"""
Hi {username},

Welcome to SwipeCollab!

Please verify your email address by clicking the link below:
{verify_url}

This link will expire in 24 hours.

If you did not create a SwipeCollab account, please ignore this email.

— The SwipeCollab Team
    """.strip()

    html_message = f"""
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="margin:0;padding:0;background:#0f0f13;font-family:Arial,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#0f0f13;padding:40px 20px;">
    <tr>
      <td align="center">
        <table width="520" cellpadding="0" cellspacing="0"
               style="background:#17171f;border:1px solid #2a2a38;border-radius:12px;overflow:hidden;">

          <!-- Header -->
          <tr>
            <td style="background:linear-gradient(135deg,#6c63ff,#a78bfa);padding:28px 32px;">
              <h1 style="margin:0;color:#fff;font-size:1.4rem;font-weight:700;letter-spacing:-0.02em;">
                SwipeCollab
              </h1>
              <p style="margin:6px 0 0;color:rgba(255,255,255,0.8);font-size:0.875rem;">
                Swipe to Collaborate
              </p>
            </td>
          </tr>

          <!-- Body -->
          <tr>
            <td style="padding:32px;">
              <h2 style="color:#f0f0f5;font-size:1.2rem;margin:0 0 12px;">
                Verify your email address
              </h2>
              <p style="color:#9898b0;font-size:0.9rem;line-height:1.6;margin:0 0 24px;">
                Hi <strong style="color:#f0f0f5;">{username}</strong>, welcome to SwipeCollab!
                Click the button below to verify your email address and activate your account.
              </p>

              <!-- Button -->
              <table cellpadding="0" cellspacing="0" style="margin:0 0 24px;">
                <tr>
                  <td style="background:#6c63ff;border-radius:8px;">
                    <a href="{verify_url}"
                       style="display:inline-block;padding:14px 28px;color:#fff;
                              font-weight:700;font-size:0.95rem;text-decoration:none;
                              letter-spacing:0.01em;">
                      Verify Email Address →
                    </a>
                  </td>
                </tr>
              </table>

              <p style="color:#5a5a75;font-size:0.8rem;line-height:1.5;margin:0;">
                If the button doesn't work, copy and paste this link into your browser:<br>
                <a href="{verify_url}" style="color:#6c63ff;word-break:break-all;">{verify_url}</a>
              </p>
            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td style="background:#0f0f13;padding:20px 32px;border-top:1px solid #2a2a38;">
              <p style="color:#5a5a75;font-size:0.78rem;margin:0;line-height:1.5;">
                This link expires in <strong>24 hours</strong>.<br>
                If you did not create a SwipeCollab account, you can safely ignore this email.
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

    print(f"==================================================")
    print(f"EMAIL VERIFICATION DISPATCH: {user.email}")
    print(f"Verify Link: {verify_url}")
    print(f"Token: {token}")
    print(f"==================================================")

    if not has_credentials:
        info_msg = "SMTP Credentials not set in environment. Generated token for in-app verification."
        print(f"SMTP skipped. {info_msg}")
        return False, info_msg

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
            print(f"Verification email sent successfully to {user.email} via SMTP.")
        except Exception as e:
            err_msg = f"SMTP error while sending to {user.email}: {str(e)}"
            print(f"==================================================")
            print(f"{err_msg}")
            print(f"Fallback Token: {token}")
            print(f"==================================================")

    thread = threading.Thread(target=_async_send, daemon=True)
    thread.start()

    return True, f"Verification email dispatch initiated for {user.email}."