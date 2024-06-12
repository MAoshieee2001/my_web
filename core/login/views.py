from django.contrib.auth import logout, login
from django.shortcuts import redirect
from django.views.generic import RedirectView, FormView

import settings
from core.login.forms import AuthenticationForm


class LoginFormView(FormView):  # Vista que permite acceder al login requerido de nuesstro aplicativo web
    form_class = AuthenticationForm
    template_name = 'login/login.html'
    success_url = settings.LOGIN_REDIRECT_URL

    def dispatch(self, request, *args, **kwargs):
        return redirect(self.success_url) if request.user.is_authenticated else super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, user=form.get_user())
        return super(LoginFormView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(LoginFormView, self).get_context_data(**kwargs)
        context['title'] = 'Iniciar Sesión'
        context['action'] = 'login'
        context['list_url'] = self.success_url
        return context


class LogoutFormView(RedirectView):
    pattern_name = 'login'

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutFormView, self).dispatch(request, *args, **kwargs)
