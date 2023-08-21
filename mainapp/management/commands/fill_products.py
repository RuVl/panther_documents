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
                p = Product(
                    title_en=passport['title'],
                    title_ru=passport['title'],
                    count=int(passport['count']),
                    cost=float(passport['usd_cost']),
                    country=country
                )
                p.file.name = 'products/test.zip'
                p.save()
