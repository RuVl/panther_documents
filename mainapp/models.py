from datetime import timedelta

from django.db import models
from django.utils.timezone import now
from django.utils.translation import get_language

from authapp.models import ShopUser


def in_24_hours():
    return now() + timedelta(hours=24)


class Product(models.Model):
    title_en = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)

    count = models.IntegerField()
    cost = models.FloatField()

    file = models.FileField(upload_to='products/')

    # Many to one
    country = models.ForeignKey('Country', on_delete=models.PROTECT)

    def get_title(self):
        match get_language():
            case 'ru':
                return self.title_ru
            case 'en-us':
                return self.title_en
            case _:
                raise Exception('No translation for this language!')

    class Meta:
        ordering = ['country']


class Country(models.Model):
    title_en = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)

    def get_title(self):
        match get_language():
            case 'ru':
                return self.title_ru
            case 'en-us':
                return self.title_en
            case _:
                raise Exception('No translation for this language!')

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'
