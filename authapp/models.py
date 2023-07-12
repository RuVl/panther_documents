from django.contrib.auth.models import AbstractUser
from django.db import models

from datetime import timedelta
from django.utils.timezone import now

from django.utils.translation import gettext_lazy as _


def activation_time():
    return now() + timedelta(hours=24)


class ShopUser(AbstractUser):
    email = models.EmailField(_("email address"), unique=True, blank=True)

    is_deleted = models.BooleanField(default=False)
    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expires = models.DateTimeField(default=activation_time)

    def is_activation_key_expired(self):
        return self.activation_key_expires <= now() and not self.is_deleted
