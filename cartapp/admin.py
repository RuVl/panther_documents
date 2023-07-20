from django.contrib import admin

from cartapp.models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    fields = ('title', 'file', 'email', 'user', 'usd_cost', 'date')
