from django.urls import path

from authapp.views import ShopUserRegisterView, ShopUserLoginView, office

urlpatterns = [
    path('register/', ShopUserRegisterView.as_view(), name='register'),
    path('login/', ShopUserLoginView.as_view(), name='login'),
    path('office/', office, name='office')
]
