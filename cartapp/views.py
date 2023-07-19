from django.urls import reverse_lazy
from django.views.generic import FormView

from cartapp.forms import BuyProductForm


class CartView(FormView):
    form_class = BuyProductForm
    template_name = 'cart/cart_page.html'
    success_url = reverse_lazy('main:home')


