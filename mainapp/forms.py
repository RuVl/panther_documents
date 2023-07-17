from django import forms
from captcha.fields import ReCaptchaField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from mainapp.models import Transaction


class SendLinksForm(forms.Form):
    email = forms.EmailField()
    captcha = ReCaptchaField()

    def clean_email(self):
        email = self.cleaned_data['email']
        if not Transaction.objects.filter(email=email).exists():
            raise ValidationError(_('Email not found'), code='not found')

        return email
