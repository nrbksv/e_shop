from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import CreateView, ListView

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


class UserStatisticsView(LoginRequiredMixin, ListView):
    template_name = 'registration/user_stat.html'
    context_object_name = 'user_obj'

    def get_queryset(self):
        return self.request.session.get('user_stat', {})
