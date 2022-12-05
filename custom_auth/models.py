import uuid as uuid

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from model_utils import Choices
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


from custom_auth.managers import ApplicationUserManager
from custom_auth.utils import set_password_reset_expiration_time


class ApplicationUser(
    AbstractBaseUser,
    PermissionsMixin
):
    GENDER_TYPES = Choices(
        ("male", "Male"),
        ("female", "Female"),
    )
    USER_TYPE = Choices(
        ('Admin','Admin'),
        ("Solution_provider","Solution_provider"),
        ("Solution_seeker","Solution_seeker")
    )

    username_validator = UnicodeUsernameValidator()
    uuid = models.UUIDField(
        verbose_name=_('uuid'),
        unique=True,
        help_text=_('Required. A 32 hexadecimal digits number as specified in RFC 4122.'),
        error_messages={
            'unique': _('A user with that uuid already exists.'),
        },
        default=uuid.uuid4,
    )
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        blank=True,
        null=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _('A user with that username already exists.'),
        },
    )
    email = models.EmailField(_('email address'), null=True, blank=True, unique=True,
                              error_messages={'unique': _('A user with that email already exists.')}, )
    is_email_verified = models.BooleanField(_('email verified'), default=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    fullname = models.CharField(_('full name'), max_length=300, blank=True,
                                help_text=_('Full name as it was returned by social provider'))
    about = models.TextField(_('about me'), max_length=1000, blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    last_modified = models.DateTimeField(_('last modified'), auto_now=True)
    last_user_activity = models.DateTimeField(_('last activity'), default=timezone.now)
    gender = models.CharField(max_length=10, choices=GENDER_TYPES, default=GENDER_TYPES.male)
    user_type = models.CharField(max_length=40, choices=USER_TYPE, default=USER_TYPE.Admin)
    date_of_birth = models.DateField(_('date of birth'), null=True, blank=True)
    city = models.CharField(_('city'), max_length=100, null=True, blank=True)

    objects = ApplicationUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.username or self.fullname or self.email or self.first_name or str(self.uuid)


class PasswordResetId(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, db_index=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    expiration_time = models.DateTimeField(default=set_password_reset_expiration_time)

    class Meta:
        verbose_name = 'Password reset id'
