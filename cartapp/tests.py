import plisio
from django.test import SimpleTestCase

from panther_documents import settings


class PlisioTest(SimpleTestCase):
    def test_invoice(self):
        client = plisio.PlisioClient(api_key=settings.PLISIO_SECRET_KEY)
        # client.invoice()
