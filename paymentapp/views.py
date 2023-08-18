import json
import logging
from smtplib import SMTPAuthenticationError

from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseForbidden, FileResponse, HttpRequest, HttpResponseBadRequest, HttpResponse, \
    HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, TemplateView

from paymentapp import plisio
from paymentapp.forms import BuyProductForm, SendLinksForm
from paymentapp.models import Transaction, ProductFile, ProductInfo, AllowedCurrencies, PlisioGateway
from paymentapp.plisio import PlisioException, save_plisio_data, verify_hash, FiatCurrency


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
            f, _ = ProductFile.objects.get_or_create(path=product.file.path)
            ProductInfo.objects.create(
                product_file=f,
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
                response: dict = plisio.create_invoice(
                    order_name=f'Order number {transaction_id}',
                    order_number=transaction_id,
                    source_amount=t.total_cost,
                    source_currency=FiatCurrency.USD,
                    email=t.email
                )

                if response.get('status') == 'success':
                    data: dict = response.get('data')
                    if data is None:
                        # Неверный ответ от сервера
                        return HttpResponseBadRequest()

                    p = PlisioGateway(txn_id=data.get('txn_id'))
                    p.save()

                    t.plisio_gateway = p
                    t.invoice_total_sum = data.get('invoice_total_sum')
                    t.save()

                    return HttpResponseRedirect(data.get('invoice_url'))
            except PlisioException as e:
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
class PlisioStatus(View):
    def post(self, request: HttpRequest, *args, **kwargs):
        data: dict = json.loads(request.body)
        if not verify_hash(data):
            return HttpResponseBadRequest()

        logging.info(f"{data.get('order_number')}: {data.get('status')}")
        match data.get('status'):
            case 'completed' | 'mismatch':
                p = PlisioGateway.objects.get(txn_id=data.get('txn_id'), transaction__pk=data.get('order_number'))
                save_plisio_data(p, data)
                SendLinksFormView.send_transaction_links([p.transaction], self.request.get_host(), p.transaction.email)
            case 'expired':
                p = PlisioGateway.objects.get(txn_id=data.get('txn_id'), transaction__pk=data.get('order_number'))
                if data.get('source_amount') >= p.transaction.invoice_total_sum:
                    save_plisio_data(p, data)
                    SendLinksFormView.send_transaction_links([p.transaction], self.request.get_host(), p.transaction.email)
                else:
                    p.invoice_closed = True
                    p.save()
            case 'cancelled':
                p = PlisioGateway.objects.get(txn_id=data.get('txn_id'), transaction__pk=data.get('order_number'))
                p.invoice_closed = True
                p.save()

        return HttpResponse()


# Вьюшка для отправки ссылок на скачивание купленных товаров
class SendLinksFormView(FormView):
    form_class = SendLinksForm
    template_name = 'payment/send_links.html'
    success_url = reverse_lazy('main:home')

    def form_valid(self, form):
        domain = self.request.get_host()
        email = form.cleaned_data['email']

        if not self.send_transaction_links(email, form.transactions, domain, self.request.scheme):
            logging.warning("Can't send email!")
            # TODO page email wasn't sent
            return self.form_invalid(form)

        return super().form_valid(form)

    @staticmethod
    def send_transaction_links(email: str, transactions: list[Transaction], domain: str, scheme: str) -> bool:
        title = f'Купленные товары на сайте {domain}'
        message = 'Наименование товара - ссылка на скачивание\n'

        for t in transactions:
            for i, f in enumerate(t.productinfo_set.all()):
                message += f'{i + 1}) {f.title} - {scheme}://{domain}{f.get_download_url()}\n'

        try:
            return send_mail(title, message, None, [email], fail_silently=False)
        except SMTPAuthenticationError as e:
            logging.error(str(e))

        return False  # Что-то не так с отправкой почтой


# Вьюшка для скачивания товаров
class DownloadLinksView(View):
    def get(self, request, *args, **kwargs):
        email = self.kwargs.get('email')
        security_code = self.kwargs.get('security_code')

        if email is None or security_code is None:
            return HttpResponseNotFound()

        try:
            product_info = ProductInfo.objects.get(transaction__email=email, security_code=security_code)
        except ProductInfo.DoesNotExist:
            return HttpResponseForbidden()

        return FileResponse(open(product_info.product_file.path, 'rb'))
