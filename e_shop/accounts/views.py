from django.contrib.auth import get_user_model, login
from django.shortcuts import reverse, redirect
from django.views.generic import CreateView

from accounts.forms import RegisterForm


class UserRegisterView(CreateView):
    template_name = 'registration/register.html'
    form_class = RegisterForm
    model = get_user_model()

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.get_success_url())

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if not next_url:
            next_url = self.request.POST.get('next')
        if not next_url:
            next_url = 'shop:product-list'
        return next_url
