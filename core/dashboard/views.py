import json
from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, DecimalField
from django.db.models.functions import Coalesce
from django.http import HttpResponse
from django.views.generic import TemplateView

from core.pos.models import Sale, Product

MODULE_NAME = 'Dashboard'


class DashboardTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'panel.html'

    def get(self, request, *args, **kwargs):
        request.user.set_group_session()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'get_graph_donut':
                data = []
                for product in Product.objects.all():
                    result = float(product.detailsale_set.all().aggregate(result=Coalesce(Sum('subtotal'), 0.00, output_field=DecimalField())).get('result'))
                    if result > 0:
                        data.append({
                            'name': product.names,
                            'y': result
                        })
            elif action == 'get_graph_bar':
                data = []
                year = datetime.now().year
                queryset = Sale.objects.filter(date_joined__year=year)
                for month in range(1, 13):
                    total = queryset.filter(date_joined__month=month).aggregate(result=Coalesce(Sum('total'), 0.00, output_field=DecimalField())).get('result')
                    data.append(float(total))
            else:
                data['error'] = 'No ha ingresado ninguna opción.'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super(DashboardTemplateView, self).get_context_data(**kwargs)
        context['title'] = 'Panel de control'
        context['entity'] = MODULE_NAME
        context['sales'] = Sale.objects.all().order_by('-id')[:5]
        return context
