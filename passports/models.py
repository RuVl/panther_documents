from django.db import models


# Create your models here.
class Passports(models.Model):
    title = models.CharField(max_length=255)
    count = models.IntegerField()

    ruble_cost = models.IntegerField()
    dollar_cost = models.IntegerField()

    country = models.ForeignKey('Country', on_delete=models.PROTECT)


class Country(models.Model):
    title = models.CharField(max_length=255)
