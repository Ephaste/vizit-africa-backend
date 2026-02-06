from django.conf import settings
from django.core.mail import send_mail

def send_verification_email(recipient_email, code):
    subject = "Verify your account"
    message = f"Hello,\n\nYour verification code is: {code}\n\nThank you for registering."
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [recipient_email]

    # send_mail returns the number of successfully delivered messages (0 or 1)
    return send_mail(subject, message, from_email, recipient_list)
