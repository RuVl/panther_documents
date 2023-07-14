from django.core.management.base import BaseCommand

from ._utils import load_from_json
from mainapp.models import Product, Country


class Command(BaseCommand):
    def handle(self, *args, **options):
        data = load_from_json('passports.json')
        Product.objects.all().delete()
        Country.objects.all().delete()

        for country_title, passports in data.items():
            country = Country(title=country_title)
            country.save()
            for passport in passports:
                Product(
                    title=passport['title'],
                    count=int(passport['count']),
                    rub_cost=float(passport['rub_cost']),
                    usd_cost=float(passport['usd_cost']),
                    country=country
                ).save()
