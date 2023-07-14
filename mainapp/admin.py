from django.contrib import admin

from mainapp.models import Product, Country


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    pass
