from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from django.views.generic import CreateView

from accounts.forms import RegisterForm


class UserRegisterView(CreateView):
    template_name = 'registration/register.html'
    form_class = RegisterForm
    model = get_user_model()

    def get_success_url(self):
        return reverse('shop:product-list')