from django.db import models


# Create your models here.
class Passport(models.Model):
    title = models.CharField(max_length=255)
    count = models.IntegerField()

    ruble_cost = models.FloatField()
    dollar_cost = models.FloatField()

    country = models.ForeignKey('Country', on_delete=models.PROTECT)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['country', 'title']
        verbose_name = 'Passport'
        verbose_name_plural = 'Passports'


class Country(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'

