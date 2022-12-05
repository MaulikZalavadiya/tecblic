from pyexpat import model
from django.db import models
from custom_auth.models import ApplicationUser
from django.utils.translation import ugettext_lazy as _



class Otp(models.Model):
    email = models.EmailField(_('email address'), null=True, blank=False, unique=True,
                              error_messages={
                                  'unique': _('A user with that email already exists.'),
                              },
                              )
    is_email_verified = models.BooleanField('email verified', default=False)
    otp = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        verbose_name = _('Otp')
        verbose_name_plural = _('Otp')

    def __str__(self):
        return self.email or self.otp or self.is_email_verified