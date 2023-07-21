import logging

from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseForbidden, FileResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView

from paymentapp.forms import BuyProductForm, SendLinksForm
from paymentapp.models import Transaction


class CartView(FormView):
    form_class = BuyProductForm
    template_name = 'payment/cart_page.html'
    success_url = reverse_lazy('payment:plisio')

    def form_valid(self, form):
        # Send success code and url as json
        response_data = {
            'success': True,
            'success_url': self.get_success_url()
        }
        return JsonResponse(response_data, json_dumps_params={'ensure_ascii': False})

    def form_invalid(self, form):
        # Send only errors in form as json
        response_data = {
            'success': False,
            'errors': form.errors
        }
        return JsonResponse(response_data, json_dumps_params={'ensure_ascii': False})


class PlisioView(View):
    pass


class SendLinksFormView(FormView):
    form_class = SendLinksForm
    template_name = 'main/get_files.html'
    success_url = reverse_lazy('main:home')

    def form_valid(self, form):
        domain = self.request.META["HTTP_HOST"]
        email = form.cleaned_data['email']
        transactions = Transaction.objects.filter(email=email).all()

        title = f'Купленные товары на сайте {domain}'
        message = 'Наименование товара - ссылка на скачивание\n'

        for t in transactions:
            message += f'{t.title} - {domain}{t.get_download_url()}\n'

        if not send_mail(title, message, None, [email], fail_silently=False):
            logging.warning("Can't send email!")
            # TODO page email wasn't sent

        return super().form_valid(form)


class DownloadLinksView(View):
    def get(self, request, *args, **kwargs):
        email = self.kwargs.get('email')
        security_code = self.kwargs.get('security_code')

        if email is None:
            return HttpResponseNotFound()

        try:
            transaction = Transaction.objects.get(email=email, security_code=security_code)
        except Transaction.DoesNotExist:
            return HttpResponseForbidden()

        return FileResponse(open(transaction.file, 'rb'))
