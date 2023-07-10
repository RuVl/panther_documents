from django.urls import path

from .views import BookListView

app_name = 'main'

urlpatterns = [
    path('', BookListView.as_view(), name='home'),
]
