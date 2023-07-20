from django.urls import path

from .views import CartView, SendLinksFormView, DownloadLinksView

app_name = 'cart'

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('get-file/', SendLinksFormView.as_view(), name='send-links'),
    path('get-file/<str:email>/<str:security_code>', DownloadLinksView.as_view(), name='download')
]
