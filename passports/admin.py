from django.contrib import admin

from passports.models import Passport, Country


@admin.register(Passport, Country)
class PassportAdmin(admin.ModelAdmin):
    pass
