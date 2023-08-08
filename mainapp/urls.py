from django.urls import path
from django.views.decorators.cache import cache_page

from .views import BookListView, page_not_found

app_name = 'main'

urlpatterns = [
    path('', cache_page(60*60)(BookListView.as_view()), name='home')
]

# Works only when DEBUG = False
handler404 = page_not_found
