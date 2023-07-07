from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView

from authapp.forms import ShopUserRegisterForm, ShopUserLoginForm


class ShopUserRegisterView(CreateView):
    form_class = ShopUserRegisterForm
    template_name = 'auth/register.html'
    success_url = reverse_lazy('auth:login')


class ShopUserLoginView(LoginView):
    form_class = ShopUserLoginForm
    template_name = 'auth/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fields'] = '__all__'
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            self.form_valid(form)
            return HttpResponseRedirect(reverse('auth:office'))
        else:
            self.form_invalid(form)
            return HttpResponseRedirect(reverse('auth:login'))


@login_required
def office(request):
    return render(request, 'auth/office.html')
