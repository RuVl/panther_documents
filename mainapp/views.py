from django.shortcuts import render
from django.views.generic import ListView, TemplateView

from mainapp.models import Country

'''
ListView - данные о каждой записи модели
DetailedView - данные о конкретной записи в бд
CreateView - создание записи с помощью формы
'''


class BookListView(ListView):
    queryset = Country.objects.exclude(product__count=0)
    template_name = 'main/products.html'
    context_object_name = 'country_list'  # Переменная в шаблоне для модели

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lang'] = 'ru'
        context['title'] = 'PantherDoc'
        return context


class SupportView(TemplateView):
    template_name = 'main/support.html'


# noinspection PyUnusedLocal
def page_not_found(request, exception):
    return render(request, '404.html', status=404)
