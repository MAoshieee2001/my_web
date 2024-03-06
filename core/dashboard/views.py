from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

MODULE_NAME = 'Dashboard'


class DashboardTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'panel.html'

    def get(self, request, *args, **kwargs):
        request.user.set_group_session()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DashboardTemplateView, self).get_context_data(**kwargs)
        context['title'] = 'Panel de control'
        context['entity'] = MODULE_NAME
        return context
