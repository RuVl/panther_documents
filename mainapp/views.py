from django.http import FileResponse, HttpRequest
from django.views.generic import ListView, TemplateView

from authapp.models import Transaction
from mainapp.models import Country

'''
ListView - данные о каждой записи модели
DetailedView - данные о конкретной записи в бд
CreateView - создание записи с помощью формы
'''


class BookListView(ListView):
    model = Country
    template_name = 'main/products.html'
    context_object_name = 'country_list'  # Переменная в шаблоне для модели

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lang'] = 'ru'
        context['title'] = 'PantherDoc'
        return context


# Test view
class GetFiles(TemplateView):
    template_name = 'main/get_files.html'

    def post(self, request: HttpRequest, *args, **kwargs):
        # Находим транзакции с этим емэйлом и высылаем на почту
        email = request.POST['email']
        transaction = Transaction.objects.get(email=email)
        return FileResponse(open(transaction.file, 'rb'))
