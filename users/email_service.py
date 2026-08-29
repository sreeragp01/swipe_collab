import json
import logging
import urllib.request
import urllib.error
import threading
from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


def send_transactional_email(subject, plain_message, html_message, recipient_email):
    """
    Dispatches transactional email using the most reliable method available:
    1. Resend API (HTTPS Port 443 - works 100% on Render free tier, never blocked)
    2. Brevo API (HTTPS Port 443 - works 100% on Render free tier, never blocked)
    3. SendGrid API (HTTPS Port 443)
    4. Standard SMTP (Works on local machines, VPS, and platforms with open SMTP ports)
    """
    resend_api_key = getattr(settings, 'RESEND_API_KEY', None)
    brevo_api_key = getattr(settings, 'BREVO_API_KEY', None)
    sendgrid_api_key = getattr(settings, 'SENDGRID_API_KEY', None)
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'SwipeCollab <onboarding@resend.dev>')

    # 1. Resend API (HTTPS)
    if resend_api_key:
        try:
            url = "https://api.resend.com/emails"
            headers = {
                "Authorization": f"Bearer {resend_api_key}",
                "Content-Type": "application/json",
                "User-Agent": "SwipeCollab-App/1.0"
            }
            sender = from_email if ('@' in from_email and not any(x in from_email for x in ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com'])) else 'SwipeCollab <onboarding@resend.dev>'
            payload = json.dumps({
                "from": sender,
                "to": [recipient_email],
                "subject": subject,
                "html": html_message,
                "text": plain_message
            }).encode('utf-8')

            req = urllib.request.Request(url, data=payload, headers=headers, method='POST')
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.status in (200, 201):
                    logger.info(f"Email successfully dispatched via Resend API to {recipient_email}")
                    print(f"[SUCCESS] Email delivered to {recipient_email} via Resend API!")
                    return True, "Email sent via Resend API."
        except Exception as e:
            logger.error(f"Resend API error: {str(e)}")
            print(f"[ERROR] Resend API error: {str(e)}")

    # 2. Brevo (Sendinblue) API (HTTPS)
    if brevo_api_key:
        try:
            url = "https://api.brevo.com/v3/smtp/email"
            headers = {
                "api-key": brevo_api_key,
                "Content-Type": "application/json",
                "User-Agent": "SwipeCollab-App/1.0"
            }
            sender_email = getattr(settings, 'EMAIL_HOST_USER', '') or 'noreply@swipecollab.com'
            payload = json.dumps({
                "sender": {"name": "SwipeCollab", "email": sender_email},
                "to": [{"email": recipient_email}],
                "subject": subject,
                "htmlContent": html_message,
                "textContent": plain_message
            }).encode('utf-8')

            req = urllib.request.Request(url, data=payload, headers=headers, method='POST')
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.status in (200, 201):
                    logger.info(f"Email successfully dispatched via Brevo API to {recipient_email}")
                    print(f"[SUCCESS] Email delivered to {recipient_email} via Brevo API!")
                    return True, "Email sent via Brevo API."
        except Exception as e:
            logger.error(f"Brevo API error: {str(e)}")
            print(f"[ERROR] Brevo API error: {str(e)}")

    # 3. Standard SMTP (Local / Unblocked hosts)
    has_smtp = bool(getattr(settings, 'EMAIL_HOST_USER', None) and getattr(settings, 'EMAIL_HOST_PASSWORD', None))
    if has_smtp:
        try:
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient_email],
                html_message=html_message,
                fail_silently=False,
            )
            print(f"[SUCCESS] Email delivered to {recipient_email} via SMTP!")
            return True, "Email sent via SMTP."
        except Exception as e:
            logger.error(f"SMTP error to {recipient_email}: {str(e)}")
            print(f"[SMTP Notice] SMTP delivery error (Render blocks outbound ports 587/465): {str(e)}")
            return False, f"SMTP error: {str(e)}"

    return False, "No email credentials configured."


def send_email_async(subject, plain_message, html_message, recipient_email):
    """
    Fires off email dispatch in a background thread so the HTTP view returns immediately.
    """
    thread = threading.Thread(
        target=send_transactional_email,
        args=(subject, plain_message, html_message, recipient_email),
        daemon=True
    )
    thread.start()
    return True
