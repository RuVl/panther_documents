from django.test import TestCase

from mainapp.models import Product, Country


# Create your tests here.
# noinspection PyMethodMayBeStatic
class ProductTest(TestCase):
    def test_files_url(self):
        c = Country(title='TEST')
        c.save()

        product = Product(count=3, title='test', usd_cost=5, rub_cost=40, country=c, file='products/test.zip')
        product.save()

        print(product.file.url)
