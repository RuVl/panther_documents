from django.views.generic import ListView
from django.shortcuts import render
from mainapp.models import Passport, Country

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


def error_404_view(request, exception):
    return render(request, '404.html')