from django.core.mail import send_mail
from django.conf import settings
from templated_email import send_templated_mail


def send_mail_otp(email,otp):
    try:
        send_templated_mail(
                        template_name='email/registration-otp',
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[email],
                        context={
                            'subject': "Order has been placed successfully",
                            'otp': f"your registration OTP {otp}"
                        },
        )
        return True
    except:
        return False 