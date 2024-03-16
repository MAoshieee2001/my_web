import json

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from core.pos.models import Logs

MODULE_NAME = 'Bitácora'


class LogTemplateView(TemplateView):
    template_name = 'log/list.html'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'get_logs':
                logs = Logs.objects.all()
                data = [log.toJSON() | {'position': position} for position, log in enumerate(logs, start=1)]
            else:
                data['error'] = 'No ha ingresado ninguna opción.'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super(LogTemplateView, self).get_context_data(**kwargs)
        context['title'] = 'Listado de Bitácoras'
        context['entity'] = MODULE_NAME
        context['list_url'] = reverse_lazy('pos:log_list')
        return context
