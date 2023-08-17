import hashlib
import hmac
from collections import OrderedDict

from panther_documents.settings import PLISIO_SECRET_KEY
from paymentapp.models import PlisioGateway


def verify_hash(data: dict) -> bool:
    temp = OrderedDict(sorted(data.items()))
    verify_hash = temp.pop('verify_hash')
    hashed = hmac.new(PLISIO_SECRET_KEY, temp, hashlib.sha1)
    return hashed.hexdigest() == verify_hash


def save_plisio_data(plisio: PlisioGateway, data: dict):
    plisio.amount = float(data.get('amount'))
    plisio.net_profit = float(data.get('invoice_sum'))
    plisio.currency = data.get('currency')
    plisio.commission = float(data.get('invoice_commission'))

    plisio.comment = data.get('plisio_comment')
    plisio.confirmations = data.get('confirmations')

    plisio.invoice_closed = True
    plisio.transaction.is_sold = True

    plisio.save()
