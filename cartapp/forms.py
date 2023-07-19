from django import forms

from mainapp.models import Product


class BuyProductForm(forms.Form):
    email = forms.EmailField()
    products = forms.ModelMultipleChoiceField(Product.objects.filter(count__gt=0))
