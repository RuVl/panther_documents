from django.contrib import admin

from mainapp.models import Product, Country, Transaction


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    pass


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    fields = ('title', 'file', 'email', 'user', 'usd_cost', 'date')
