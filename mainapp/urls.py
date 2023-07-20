from django.urls import path

from .views import BookListView, page_not_found

app_name = 'main'

urlpatterns = [
    path('', BookListView.as_view(), name='home')
]

# Works only when DEBUG = False
handler404 = page_not_found
