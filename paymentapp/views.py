import hashlib
import hmac
import json
import logging
from collections import OrderedDict

import plisio
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseForbidden, FileResponse, HttpRequest, HttpResponseBadRequest, HttpResponse, \
    HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, TemplateView
from plisio.exceptions import PlisioAPIException, PlisioRequestException

from panther_documents import settings
from paymentapp.forms import BuyProductForm, SendLinksForm
from paymentapp.models import Transaction, ProductFile, ProductInfo, AllowedCurrencies, PlisioGateway


# Вьюшка для отображения корзины и переадресации на оплату
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
        t = Transaction(email=form.cleaned_data['email'], gateway=form.cleaned_data['gateway'])
        if self.request.user.is_authenticated:
            t.user_id = self.request.user.id
        t.save()  # Без сохранения не установить m2m rel

        # Привязываем файлы к транзакции и считаем сумму
        for product in form.cleaned_data['products']:
            t.total_cost += product.usd_cost
            f, _ = ProductFile.objects.get_or_create(file=product.file.path)
            ProductInfo.objects.create(
                file=f,
                transaction=t,
                cost=product.usd_cost,  # TODO cost according currency
                currency=AllowedCurrencies.USD,  # TODO currency
            )
        t.save()  # Посчитали сумму цен всех товаров

        self.success_url = t.get_gateway_url()

        # Send success code and url as json
        response_data = {
            'success': True,
            'success_url': self.success_url
        }
        return JsonResponse(response_data, json_dumps_params={'ensure_ascii': False})

    def form_invalid(self, form):
        # Send only errors in form as json
        response_data = {
            'success': False,
            'errors': form.errors
        }
        return JsonResponse(response_data, json_dumps_params={'ensure_ascii': False})


# Вьюшка для переадресации или вывода ошибки plisio
class PlisioPaymentView(TemplateView):
    template_name = 'payment/plisio.html'
    plisio_client = plisio.Client(api_key=settings.PLISIO_SECRET_KEY)

    # TODO make more private url
    def get(self, request: HttpRequest, *args, **kwargs):
        transaction_id = kwargs.pop('transaction_id', None)
        if transaction_id is None:
            return HttpResponseBadRequest()

        try:
            t = Transaction.objects.get(id=transaction_id)
        except Transaction.DoesNotExist:
            return HttpResponseNotFound()

        if t.is_sold:  # TODO already sold
            return super().get(request, *args, **kwargs)

        if t.gateway != t.PaymentMethod.PLISIO:
            return HttpResponseNotFound()  # Метод оплаты этой транзакции не plisio

        if t.plisio_gateway is None:
            try:
                data: dict = self.plisio_client.invoice(
                    order_name=f'Order number {transaction_id}',
                    order_number=transaction_id,
                    amount=None,
                    currency=None,
                    source_amount=t.total_cost,
                    source_currency=AllowedCurrencies.USD,
                    email=t.email
                )

                logging.error(f'ДАННЫЕ ПРИШЛИ {data}')

                if data.get('success') and data.get('data'):
                    p = PlisioGateway(txn_id=data['data'].get('txn_id'))
                    p.save()

                    t.plisio_gateway = p
                    t.invoice_total_sum = data['data'].get('invoice_total_sum')
                    t.save()

                    return HttpResponseRedirect(data.get('invoice_url'))

            except (PlisioAPIException, PlisioRequestException) as e:
                logging.error(str(e))

            # TODO произошла ошибка платежного шлюза, попробуйте снова
            return HttpResponseBadRequest()

        # TODO Проверка оплаты по кнопке и ссылка на оплату
        self.extra_context = {
            'action': 'button_redirect',
            'plisio_gateway': t.plisio_gateway
        }
        return super().get(request, *args, **kwargs)  # Пользователь нажал назад на странице оплаты


# Вьюшка для получения статуса транзакции plisio
class PlisioStatusView(View):
    def post(self, request: HttpRequest, *args, **kwargs):
        data: dict = json.loads(request.body)
        if not self.verify_hash(data):
            return HttpResponseBadRequest()

        logging.info(f"{data.get('order_number')}: {data.get('status')}")
        match data.get('status'):
            case 'completed' | 'mismatch':
                p = PlisioGateway.objects.get(txn_id=data.get('txn_id'), transaction__pk=data.get('order_number'))
                self.save_plisio_data(p, data)
                SendLinksFormView.send_transaction_links([p.transaction], self.request.get_host(), p.transaction.email)
            case 'expired':
                p = PlisioGateway.objects.get(txn_id=data.get('txn_id'), transaction__pk=data.get('order_number'))
                if data.get('source_amount') >= p.transaction.invoice_total_sum:
                    self.save_plisio_data(p, data)
                    SendLinksFormView.send_transaction_links([p.transaction], self.request.get_host(), p.transaction.email)
            case 'cancelled' | 'error':
                p = PlisioGateway.objects.get(txn_id=data.get('txn_id'), transaction__pk=data.get('order_number'))
                p.invoice_closed = True
                p.save()

        return HttpResponse()

    @staticmethod
    def verify_hash(data: dict) -> bool:
        temp = OrderedDict(sorted(data.items()))
        verify_hash = temp.pop('verify_hash')
        hashed = hmac.new(settings.PLISIO_SECRET_KEY, temp, hashlib.sha1)
        return hashed.hexdigest() == verify_hash

    @staticmethod
    def save_plisio_data(plisio: PlisioGateway, data: dict):
        plisio.amount = float(data.get('amount'))
        plisio.net_profit = float(data.get('invoice_sum'))
        plisio.currency = data.get('currency')
        plisio.commission = float(data.get('invoice_commission'))

        plisio.comment = data.get('plisio_comment')
        plisio.confirmations = data.get('confirmations')

        plisio.invoice_closed = True
        plisio.transaction.is_sold = True

        plisio.save()


# Вьюшка для отправки ссылок на скачивание купленных товаров
class SendLinksFormView(FormView):
    form_class = SendLinksForm
    template_name = 'payment/send_links.html'
    success_url = reverse_lazy('main:home')

    def form_valid(self, form):
        domain = self.request.get_host()
        email = form.cleaned_data['email']
        transactions = Transaction.objects.filter(email=email, is_sold=True).all()

        if not self.send_transaction_links(transactions, domain, email):
            logging.warning("Can't send email!")
            # TODO page email wasn't sent

        return super().form_valid(form)

    @staticmethod
    def send_transaction_links(transactions: list[Transaction], domain: str, email: str) -> bool:
        title = f'Купленные товары на сайте {domain}'
        message = 'Наименование товара - ссылка на скачивание\n'

        for t in transactions:
            for i, f in enumerate(t.productinfo_set.all()):
                message += f'{i + 1}) {f.title} - {domain}{f.get_download_url()}\n'

        return send_mail(title, message, None, [email], fail_silently=False)


# Вьюшка для скачивания товаров
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
