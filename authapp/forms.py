import hashlib
import random

from captcha.fields import ReCaptchaField
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from authapp.models import ShopUser


class ShopUserRegisterForm(UserCreationForm):
    captcha = ReCaptchaField()

    class Meta:
        model = ShopUser
        fields = ('email', 'username', 'password1', 'password2')

    def save(self, **kwargs):
        user = super().save(kwargs)

        # Generate activation key
        user.is_active = False  # If true - user can log in
        salt = hashlib.sha256(str(random.random()).encode('utf8')).hexdigest()
        user.activation_key = hashlib.sha256((user.email + salt).encode('utf8')).hexdigest()
        user.save()

        return user


class ShopUserLoginForm(AuthenticationForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'password')
