from django.contrib import admin

from passports.models import Passports, Country

# Register your models here.
admin.site.register(Passports)
admin.site.register(Country)
