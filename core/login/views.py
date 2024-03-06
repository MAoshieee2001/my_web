from django.contrib.auth import logout, login
from django.shortcuts import redirect
from django.views.generic import RedirectView, FormView

import settings
from core.login.forms import AuthenticationForm


class LoginFormView(FormView):
    form_class = AuthenticationForm
    template_name = 'login/login.html'
    success_url = settings.LOGIN_REDIRECT_URL

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, user=form.get_user())
        return super(LoginFormView, self).form_valid(form)

    '''   
     def post(self, request, *args, **kwargs):
            data = {}
            try:
                action = request.POST['action']
                if action == 'login':
                    form = self.get_form()
                    if form.is_valid():
                        login(self.request, user=form.get_user())
                    else:
                        data['error'] = form.errors
                else:
                    data['error'] = 'No ha ingresado ninguna opción.'
            except Exception as e:
                data['error'] = str(e)
            return HttpResponse(json.dumps(data), content_type='application/json')
    '''

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
