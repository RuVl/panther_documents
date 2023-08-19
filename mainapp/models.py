from datetime import timedelta

from django.db import models
from django.utils.timezone import now

from authapp.models import ShopUser


def in_24_hours():
    return now() + timedelta(hours=24)


class Product(models.Model):
    # title_en = models.CharField(max_length=255)
    # title_ru = models.CharField(max_length=255)
    title = models.CharField(max_length=255)

    count = models.IntegerField()

    rub_cost = models.FloatField()
    usd_cost = models.FloatField()

    file = models.FileField(upload_to='products/')

    # Many to one
    country = models.ForeignKey('Country', on_delete=models.PROTECT)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['country']


class Country(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'
