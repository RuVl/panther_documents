from captcha.fields import ReCaptchaField
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _\

from cartapp.models import Transaction
from mainapp.models import Product


class BuyProductForm(forms.Form):
    email = forms.EmailField()
    products = forms.ModelMultipleChoiceField(Product.objects.filter(count__gt=0))


class SendLinksForm(forms.Form):
    email = forms.EmailField()
    captcha = ReCaptchaField()

    def clean_email(self):
        email = self.cleaned_data['email']
        if not Transaction.objects.filter(email=email).exists():
            raise ValidationError(_('Email not found'), code='not found')

        return email
