from django.urls import path
from django.conf.urls import handler404
from .views import BookListView, cart_page

app_name = 'main'

urlpatterns = [
    path('', BookListView.as_view(), name='home'),
    path('cart', cart_page)
]

handler404 = 'mainapp.views.error_404_view'
