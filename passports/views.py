from django.views.generic import ListView

from passports.models import Passport, Country

'''
ListView - данные о каждой записи модели
DetailedView - данные о конкретной записи в бд
CreateView - создание записи с помощью формы
'''


class BookListView(ListView):
    model = Passport
    template_name = 'passports/test.html'
    # context_object_name = 'countries'  # Переменная в шаблоне для модели

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lang'] = 'ru'
        context['title'] = 'PantherDoc'
        return context
