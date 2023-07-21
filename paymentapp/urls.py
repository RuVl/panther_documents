from django.urls import path

from .views import CartView, SendLinksFormView, DownloadLinksView, PlisioView

app_name = 'payment'

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('plisio/', PlisioView.as_view(), name='plisio'),
    path('get-file/', SendLinksFormView.as_view(), name='send-links'),
    path('get-file/<str:email>/<str:security_code>', DownloadLinksView.as_view(), name='download')
]
