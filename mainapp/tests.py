from django.test import TestCase

from mainapp.models import Product, Country


# Create your tests here.
# noinspection PyMethodMayBeStatic
class ProductTest(TestCase):
    def test_country_filter(self):
        c = Country(title='TEST')
        c.save()

        product = Product(count=0, title='test', usd_cost=5, rub_cost=40, country=c, file='products/test.zip')
        product.save()

        self.assertEquals(Country.objects.filter(product__count__gt=0).count(), 0)
