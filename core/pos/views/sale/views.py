import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, DeleteView

from core.pos.forms import SaleForm, CustomerForm
from core.pos.models import Sale, Customer, Product, DetailSale

MODULE_NAME = 'Venta'


class SaleTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'sale/list.html'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'get_sales':
                data = [sale.toJSON() | {'position': position} for position, sale in enumerate(Sale.objects.all(), start=1)]
            elif action == 'get_details':
                id_sale = request.POST['id_sale']
                details = DetailSale.objects.filter(sale_id=id_sale)
                data = [detail.toJSON() for detail in details]
            else:
                data['error'] = 'No ha ingresado ninguna opción.'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super(SaleTemplateView, self).get_context_data(**kwargs)
        context['title'] = 'Listado de Venta'
        context['entity'] = MODULE_NAME
        context['create_url'] = reverse_lazy('pos:sale_create')
        context['list_url'] = reverse_lazy('pos:sale_list')
        return context


class SaleCreateView(LoginRequiredMixin, CreateView):
    model = Sale
    form_class = SaleForm
    template_name = 'sale/create.html'
    success_url = reverse_lazy('pos:sale_list')

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'create':
                products = json.loads(request.POST['products'])
                with transaction.atomic():
                    sale = Sale()
                    sale.customer_id = int(request.POST['customer'])
                    sale.employee = request.user
                    sale.iva = float(request.POST['iva'])
                    sale.cash = float(request.POST['cash'])
                    sale.save()
                    for product in products:
                        detail = DetailSale()
                        detail.sale = sale
                        detail.product_id = product['id']
                        detail.quantity = int(product['cant'])
                        detail.price = float(product['pvp'])
                        detail.subtotal = detail.quantity * detail.price
                        detail.save()
                        detail.product.stock -= detail.quantity
                        detail.product.save()
                    sale.calcule_invoice()
            elif action == 'get_cutomers_select2':
                term = request.POST.get('term', '')
                customers = Customer.objects.all()
                if term:
                    customers = customers.filter(Q(first_names__icontains=term) | Q(last_names__icontains=term) |
                                                 Q(dni__icontains=term))
                data = [customer.toJSON() | {'text': customer.get_full_names_DNI()} for customer in customers[0:10]]
            elif action == 'get_products_autocomplete':
                ids_exclude = json.loads(request.POST['products_id'])
                term = request.POST.get('term', '')
                products = Product.objects.filter(stock__gt=0)
                if term:
                    products = products.filter(Q(names__icontains=term) | Q(category__names__icontains=term) | Q(code__icontains=term))
                data = [product.toJSON() | {'value': product.names} for product in products.exclude(id__in=ids_exclude)[0:5]]
            elif action == 'get_products_data':
                ids_exclude = json.loads(request.POST['products_id'])
                products = Product.objects.filter(stock__gt=0)
                data = [product.toJSON() for product in products.exclude(id__in=ids_exclude)]
            elif action == 'create_customer':
                customer = CustomerForm(request.POST)
                data = customer.save()
            else:
                data['error'] = 'No ha ingressado ninguna opción.'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super(SaleCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Creación de Venta'
        context['entity'] = MODULE_NAME
        context['action'] = 'create'
        context['list_url'] = self.success_url
        context['frmCustomer'] = CustomerForm()
        return context


class SaleDeleteView(LoginRequiredMixin, DeleteView):
    model = Sale
    template_name = 'delete.html'
    success_url = reverse_lazy('pos:sale_list')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(SaleDeleteView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'delete':
                for detail in self.object.detailsale_set.all():
                    detail.product.stock += detail.quantity
                    detail.product.save()
                    self.object.delete()
            else:
                data['error'] = 'No ha ingresado ninguna opción.'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super(SaleDeleteView, self).get_context_data(**kwargs)
        context['title'] = 'Eliminación de Venta'
        context['entity'] = MODULE_NAME
        context['action'] = 'delete'
        context['list_url'] = self.success_url
        return context
