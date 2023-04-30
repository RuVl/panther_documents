from django.core.management.base import BaseCommand

from ._utils import load_from_json
from main.models import Passport, Country


class Command(BaseCommand):
    def handle(self, *args, **options):
        data = load_from_json('passports.json')
        Passport.objects.all().delete()
        Country.objects.all().delete()

        for country_title, passports in data.items():
            country = Country(title=country_title)
            country.save()
            for passport in passports:
                Passport(
                    title=passport['title'],
                    count=int(passport['count']),
                    ruble_cost=float(passport['rub_cost']),
                    dollar_cost=float(passport['usd_cost']),
                    country=country
                ).save()
