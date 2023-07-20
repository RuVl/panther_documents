from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import FormView

from cartapp.forms import BuyProductForm


class CartView(FormView):
    form_class = BuyProductForm
    template_name = 'cart/cart_page.html'
    success_url = reverse_lazy('main:home')

    def form_valid(self, form):
        response_data = {
            'success': True,
            'success_url': self.success_url
        }
        return JsonResponse(response_data, json_dumps_params={'ensure_ascii': False})

    def form_invalid(self, form):
        response_data = {
            'success': False,
            'errors': [(k, v) for k, v in form.errors.items()]
        }
        return JsonResponse(response_data, json_dumps_params={'ensure_ascii': False})
