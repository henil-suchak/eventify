from django.core.mail import EmailMessage
from django.conf import settings

def send_dynamic_email(subject, message, sender_email, recipients):
    """
    Sends an email dynamically using the sender's email as the reply-to.
    """
    try:
        email = EmailMessage(
            subject,
            message,
            sender_email,  # Sender must match your SMTP email
            recipients,
            headers={"Reply-To": sender_email},  # Reply-To set to actual sender
        )
        email.send(fail_silently=False)
        return True  # Email sent successfully
    except Exception as e:
        print(f"Error sending email: {e}")
        return False  # Email failed