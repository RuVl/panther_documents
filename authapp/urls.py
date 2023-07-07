from django.urls import path

from authapp.views import ShopUserRegisterView, ShopUserLoginView, office

app_name = 'authapp'

urlpatterns = [
    path('register/', ShopUserRegisterView.as_view(), name='register'),
    path('login/', ShopUserLoginView.as_view(), name='login'),
    path('office/', office, name='office')
]
