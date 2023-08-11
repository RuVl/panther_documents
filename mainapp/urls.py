from django.urls import path
from django.views.decorators.cache import cache_page

from .views import BookListView, SupportView, page_not_found

app_name = 'main'

urlpatterns = [
    path('', cache_page(60*60)(BookListView.as_view()), name='home'),
    path('support/', cache_page(60*60)(SupportView.as_view()), name='support')
]

# Works only when DEBUG = False
handler404 = page_not_found
