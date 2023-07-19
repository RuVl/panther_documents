import logging

from django.core.mail import send_mail
from django.http import FileResponse, HttpRequest, HttpResponseNotFound, HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, TemplateView, FormView

from mainapp.forms import SendLinksForm
from mainapp.models import Country, Transaction

'''
ListView - данные о каждой записи модели
DetailedView - данные о конкретной записи в бд
CreateView - создание записи с помощью формы
'''


class BookListView(ListView):
    model = Country
    template_name = 'main/products.html'
    context_object_name = 'country_list'  # Переменная в шаблоне для модели

    def get_queryset(self):
        return Country.objects.filter(product__count__gt=0)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lang'] = 'ru'
        context['title'] = 'PantherDoc'
        return context


# noinspection PyUnusedLocal
def page_not_found(request, exception):
    return render(request, '404.html', status=404)


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


class GetFiles(TemplateView):
    template_name = 'main/get_files.html'

    def post(self, request: HttpRequest, *args, **kwargs):
        # Находим транзакции с этим емэйлом и высылаем на почту
        email = request.POST['email']
        transaction = Transaction.objects.get(email=email)
        return FileResponse(open(transaction.file, 'rb'))


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
