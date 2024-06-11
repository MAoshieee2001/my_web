import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import FormView

from core.pos.mixins import ValidatePermissionRequiredMixin
from core.pos.models import Sale
from core.reports.forms import ReportSaleForm

MODULE_NAME = 'Venta'


class ReportSaleTemplateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, FormView):
    form_class = ReportSaleForm
    permission_required = 'view_sale'
    template_name = 'sale/report.html'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'get_sales':
                start_date = request.POST['start_date']
                end_date = request.POST['end_date']
                sales = Sale.objects.all()
                if len(start_date) and len(end_date):
                    sales = sales.filter(date_joined__range=[start_date, end_date])
                data = [sale.toJSON() | {'position': position} for position, sale in enumerate(sales, start=1)]
            else:
                data['error'] = 'No ha ingresado ninguna opción.'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super(ReportSaleTemplateView, self).get_context_data(**kwargs)
        context['title'] = 'Reporte de Venta'
        context['entity'] = MODULE_NAME
        context['list_url'] = reverse_lazy('dashboard')
        return context
