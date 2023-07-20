import hashlib
import random
from datetime import timedelta

from django.db import models
from django.urls import reverse_lazy
from django.utils.timezone import now

from authapp.models import ShopUser
from panther_documents import settings


def in_24_hours():
    return now() + timedelta(hours=24)


class Transaction(models.Model):
    # What was sold
    title = models.CharField(max_length=255)
    file = models.FilePathField(path=settings.MEDIA_ROOT / 'products', max_length=255)

    # Who bought
    email = models.EmailField()
    user = models.ForeignKey(ShopUser, on_delete=models.SET_NULL, blank=True, null=True)

    usd_cost = models.FloatField()  # Cost
    date = models.DateTimeField()  # When was sold

    # For email sending
    security_code = models.CharField(max_length=128, blank=True, null=True)
    security_code_expires = models.DateTimeField(default=in_24_hours, blank=True, null=True)

    def is_security_code_expired(self) -> bool:
        return not self.security_code or self.security_code_expires <= now()

    def get_download_url(self):
        if self.is_security_code_expired():
            self.security_code_expires = in_24_hours()
            salt = hashlib.sha256(str(random.random()).encode('utf8')).hexdigest()
            self.security_code = hashlib.sha256((self.pk + salt).encode('utf8')).hexdigest()
            self.save()

        return reverse_lazy('cart:download', args=[self.email, self.security_code])

    class Meta:
        ordering = ['date']
