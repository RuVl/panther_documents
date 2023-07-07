from django.urls import path

from .views import BookListView

app_name = 'mainapp'

urlpatterns = [
    path('', BookListView.as_view(), name='home'),
]
