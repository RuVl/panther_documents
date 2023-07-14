from django.urls import path

from .views import BookListView, GetFiles

app_name = 'main'

urlpatterns = [
    path('', BookListView.as_view(), name='home'),
    path('get-file/', GetFiles.as_view(), name='files')
]
