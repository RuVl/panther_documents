from django.urls import path

from .views import BookListView, GetFiles, cart_page, page_not_found

app_name = 'main'

urlpatterns = [
    path('', BookListView.as_view(), name='home'),
    path('get-file/', GetFiles.as_view(), name='files'),
    path('cart', cart_page)
]

# Works only when DEBUG = False
handler404 = page_not_found
