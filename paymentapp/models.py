import hashlib
import logging
import random
from datetime import timedelta

from django.db import models
from django.urls import reverse_lazy
from django.utils.timezone import now

from authapp.models import ShopUser
from panther_documents import settings
from paymentapp.plisio import get_transaction_details, PlisioException


# Max expire period for download files
def in_7_days():
    return now() + timedelta(days=7)


# Max invoice expire period
def in_48_hours():
    return now() + timedelta(days=2)


# noinspection SpellCheckingInspection
class AllowedCurrencies(models.TextChoices):
    """ All possible currencies for purchase """
    ETH = 'ETH', 'Ethereum'
    BTC = 'BTC', 'Bitcoin'
    LTC = 'LTC', 'Litecoin'
    DASH = 'DASH', 'Dash'
    TZEC = 'TZEC', 'Zcash'
    DOGE = 'DOGE', 'Dogecoin'
    BCH = 'BCH', 'Bitcoin Cash'
    XMR = 'XMR', 'Monero'
    USDT = 'USDT', 'Tether ERC-20'
    USDC = 'USDC', 'USD Coin'
    SHIB = 'SHIB', 'Shiba Inu'
    BTT = 'BTT', 'BitTorrent TRC-20'
    USDT_TRX = 'USDT_TRX', 'Tether TRC-20'
    TRX = 'TRX', 'Tron'
    BNB = 'BNB', 'BNB Chain'
    BUSD = 'BUSD', 'Binance USD BEP-20'
    USDT_BSC = 'USDT_BSC', 'Tether BEP-20'

    USD = 'USD', '$'
    RUB = 'RUB', '₽'


class Transaction(models.Model):
    class PaymentMethod(models.TextChoices):
        PLISIO = 'PLISIO', 'plisio'

    is_sold = models.BooleanField(default=False)

    # Сумма цен всех товаров
    total_cost = models.FloatField(blank=True, default=-1)  # Required
    # Цена, которую должны заплатить
    invoice_total_sum = models.FloatField(blank=True, null=True)
    currency = models.CharField(choices=AllowedCurrencies.choices, default=AllowedCurrencies.USD)  # Override

    product_files = models.ManyToManyField('ProductFile', through='ProductInfo')  # Required

    email = models.EmailField()  # Required
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)  # Optional

    # What gateway we will use
    gateway = models.CharField(choices=PaymentMethod.choices)

    # Must be one of gateways
    plisio_gateway = models.OneToOneField('PlisioGateway', on_delete=models.SET_NULL, null=True, blank=True)

    # Переадресация в зависимости от метода оплаты
    def get_gateway_url(self):
        match self.gateway:
            case self.PaymentMethod.PLISIO:
                return reverse_lazy('payment:plisio', args=(self.id,))

    def check_if_sold(self):
        if self.is_sold:
            return True

        match self.gateway:
            case self.PaymentMethod.PLISIO:
                if self.plisio_gateway is None:
                    return False

                try:
                    response = get_transaction_details(self.plisio_gateway.txn_id)
                except PlisioException:
                    return False

                logging.error(response)

                # На всякий
                if response.get('data') is None:
                    return False

                if response['data'].get('status') in ['completed', 'mismatch']:
                    self.is_sold = True
                    self.save()
                    return True

        return False

    def __str__(self):
        return f'<Transaction {self.id}, owner {self.email}, is_sold {self.is_sold}>'


class ProductFile(models.Model):
    # Might be added info about file (title, country)
    file = models.FilePathField(path=settings.MEDIA_ROOT / 'products', max_length=255, unique=True)


class ProductInfo(models.Model):
    # Required for m2m
    file = models.ForeignKey(ProductFile, on_delete=models.SET_NULL, null=True)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)

    # Информация о товаре
    title = models.CharField(max_length=255)

    # Цена на момент покупки
    cost = models.FloatField()
    count = models.IntegerField(default=1)
    currency = models.CharField(choices=AllowedCurrencies.choices, default=AllowedCurrencies.USD)

    # Для ссылок на скачивание
    security_code = models.CharField(max_length=128, blank=True)
    security_code_expire = models.DateTimeField(default=in_7_days)

    def is_security_code_expired(self) -> bool:
        return not self.security_code or self.security_code_expires <= now()

    def get_download_url(self):
        if not self.transaction.is_sold:
            return None

        if self.is_security_code_expired():
            self.security_code_expires = in_7_days()
            salt = hashlib.sha256(str(random.random()).encode('utf8')).hexdigest()
            self.security_code = hashlib.sha256((self.pk + salt).encode('utf8')).hexdigest()
            self.save()

        return reverse_lazy('payment:download', args=[self.transaction.email, self.security_code])


class PlisioGateway(models.Model):
    invoice_expire = models.DateTimeField(default=in_48_hours)

    # Request
    invoice_closed = models.BooleanField(default=False)
    txn_id = models.CharField(max_length=255)

    # Callback
    amount = models.FloatField(null=True, blank=True)
    net_profit = models.FloatField(null=True, blank=True)
    currency = models.CharField(choices=AllowedCurrencies.choices,
                                null=True, blank=True)
    confirmations = models.CharField(null=True, blank=True)

    comment = models.CharField(max_length=255, null=True, blank=True)
    commission = models.FloatField(null=True, blank=True)

    def get_invoice_url(self):
        return f'https://plisio.net/invoice/{self.txn_id}'

    def is_invoice_expired(self):
        return self.invoice_expire <= now()
