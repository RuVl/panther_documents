from django.urls import path

from .views import CartView, SendLinksFormView, DownloadLinksView, PlisioPaymentView, PlisioStatusView

app_name = 'payment'

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('transactions/plisio/<int:transaction_id>/', PlisioPaymentView.as_view(), name='plisio'),
    path('transaction/plisio/status/', PlisioStatusView.as_view()),
    path('get-files/', SendLinksFormView.as_view(), name='send-links'),
    path('get-file/<str:email>/<str:security_code>/', DownloadLinksView.as_view(), name='download')
]
