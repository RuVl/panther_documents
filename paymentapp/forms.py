from captcha.fields import ReCaptchaField
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from paymentapp.models import Transaction
from mainapp.models import Product


class BuyProductForm(forms.Form):
    email = forms.EmailField(label=_('Email'))
    products = forms.ModelMultipleChoiceField(
        Product.objects.filter(count__gt=0),
        label=_('Choose products')
    )
    gateway = forms.ChoiceField(
        choices=Transaction.PaymentMethod.choices,
        label=_('Payment method')
    )

    def __init__(self, *, user_email=None, **kwargs):
        super().__init__(**kwargs)

        field = self.fields['products']
        field.widget = field.hidden_widget()

        if user_email is not None:
            self.fields['email'].widget.attrs.update({'value': user_email})
            self.fields['email'].widget.attrs.update({'readonly': 'true'})


class SendLinksForm(forms.Form):
    email = forms.EmailField()
    captcha = ReCaptchaField()

    def clean_email(self):
        email = self.cleaned_data['email']
        if not Transaction.objects.filter(email=email, is_sold=True).exists():
            raise ValidationError(_('Email not found'), code='not found')

        return email
