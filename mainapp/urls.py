from django.urls import path

from .views import BookListView, CartView, page_not_found, SendLinksFormView, DownloadLinksView

app_name = 'main'

urlpatterns = [
    path('', BookListView.as_view(), name='home'),
    path('get-file/', SendLinksFormView.as_view(), name='send-links'),
    path('get-file/<str:email>/<str:security_code>', DownloadLinksView.as_view(), name='download'),
    path('cart/', CartView.as_view(), name='cart')
]

# Works only when DEBUG = False
handler404 = page_not_found
