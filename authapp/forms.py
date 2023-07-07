import hashlib
import random

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from authapp.models import ShopUser


class ShopUserRegisterForm(UserCreationForm):
    class Meta:
        model = ShopUser
        fields = ('email', 'username', 'password1', 'password2')

    def save(self, **kwargs):
        user = super(ShopUserRegisterForm, self).save(kwargs)
        user.is_active = False
        salt = hashlib.sha256(str(random.random()).encode('utf8')).hexdigest()[:6]
        user.activation_key = hashlib.sha256((user.email + salt).encode('utf8')).hexdigest()
        user.save()
        return user


class ShopUserLoginForm(AuthenticationForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'password')
