from django.utils import timezone


def set_password_reset_expiration_time():
    return timezone.now() + timezone.timedelta(days=1)
