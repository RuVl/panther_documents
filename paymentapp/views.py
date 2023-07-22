import logging

import plisio
from django.core.handlers.wsgi import WSGIRequest
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseForbidden, FileResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, TemplateView

from panther_documents import settings
from paymentapp.forms import BuyProductForm, SendLinksForm
from paymentapp.models import Transaction, ProductFile, PurchaseInfo, AllowedCurrencies


class CartView(FormView):
    form_class = BuyProductForm
    template_name = 'payment/cart_page.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.user.is_authenticated:
            kwargs['user_email'] = self.request.user.email

        return kwargs

    def form_valid(self, form):
        # Создание транзакции для дальнейшей оплаты
        t = Transaction(email=form.cleaned_data['email'])
        if self.request.user.is_authenticated:
            t.user_id = self.request.user.id
        t.save()  # Без сохранения не установить m2m rel

        # Привязываем файлы к транзакции и считаем сумму
        total = 0
        for product in form.cleaned_data['products']:
            total += product.usd_cost
            f, _ = ProductFile.objects.get_or_create(file=product.file.path)
            PurchaseInfo.objects.create(
                file=f,
                transaction=t,
                cost=product.usd_cost,  # TODO cost according currency
                currency=AllowedCurrencies.USD,  # TODO currency
            )

        # Меняем итоговую сумму
        t.total_cost = total
        t.save()

        # Переадресация в зависимости от выбранного метода оплаты
        self.success_url = reverse_lazy('payment:plisio', args=(t.id,))

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


class PlisioPaymentView(TemplateView):
    template_name = 'payment/plisio.html'
    plisio_client = plisio.Client(api_key=settings.PLISIO_SECRET_KEY)

    # TODO make more private
    def get(self, request: WSGIRequest, *args, **kwargs):
        transaction_id = kwargs.pop('transaction_id', None)
        if transaction_id is None:
            return HttpResponseNotFound()

        try:
            t = Transaction.objects.get(id=transaction_id)
        except Transaction.DoesNotExist:
            return HttpResponseNotFound()

        if t.is_sold:
            # TODO already paid
            return super().get(request, *args, **kwargs)

        if t.plisio_gateway is None:
            data = self.plisio_client.invoice(
                order_name=f"Test order",
                order_number=transaction_id,
                currency=AllowedCurrencies.USDT,
                amount=-1,  # Bcs source_amount is passed
                source_amount=t.total_cost,
                source_currency=AllowedCurrencies.USD,
                email=t.email
            )
            # PlisioGateway.objects.create()
            return JsonResponse(data)

        return super().get(request, *args, **kwargs)


class SendLinksFormView(FormView):
    form_class = SendLinksForm
    template_name = 'payment/send_links.html'
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
