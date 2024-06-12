import json
import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, TemplateView, DeleteView
from weasyprint import CSS
from weasyprint import HTML
from config import settings
from core.pos.forms import SaleForm, CustomerForm
from core.pos.mixins import ValidatePermissionRequiredMixin, CompanyIsExistMixin
from core.pos.models import Sale, Customer, Product, DetailSale, Company

MODULE_NAME = 'Venta'


class SaleTemplateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, TemplateView):
    permission_required = 'view_sale'
    template_name = 'sale/list.html'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'get_sales':
                # Capturamos nuestros campos de datatable
                start = int(request.POST.get('start', 0))
                length = int(request.POST.get('length', 10))
                term = request.POST.get('search[value]', '')
                # Obtenemos nuestro queryset
                sales = Sale.objects.all()
                # Filtramo si hay un dato entrante en search
                if term:
                    sales = sales.filter(Q(customer__first_names__icontains=term) | Q(customer__last_names__icontains=term) | Q(employee__first_name__icontains=term))
                # Utilizamo el paginator
                paginator = Paginator(sales, length)
                get_number = start // length + 1
                sales_page = paginator.page(get_number)
                data = {
                    'data': [sale.toJSON() | {'position': position} for position, sale in enumerate(sales_page, start=start + 1)],
                    'recordsTotal': paginator.count,
                    'recordsFiltered': paginator.count,
                    'draw': int(request.POST.get('draw', 1))
                }
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


class SaleCreateView(LoginRequiredMixin, CompanyIsExistMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Sale
    form_class = SaleForm
    template_name = 'sale/create.html'
    permission_required = 'add_sale'
    success_url = reverse_lazy('pos:sale_list')

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'create':
                products = json.loads(request.POST['products'])
                with transaction.atomic():
                    sale = Sale()
                    sale.company = Company.objects.first()
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
                    data = {'print_url': str(reverse_lazy('pos:sale_invoice_pdf', kwargs={'pk': sale.id}))}
            elif action == 'get_cutomers_select2':
                term = request.POST.get('term', '')
                customers = Customer.objects.all()
                if term:
                    customers = customers.filter(Q(first_names__icontains=term) | Q(last_names__icontains=term) | Q(dni__icontains=term))
                data = [customer.toJSON() | {
                    'text': customer.get_full_names_DNI()} for customer in customers[0:10]]
            elif action == 'get_products_autocomplete':
                ids_exclude = json.loads(request.POST['products_id'])
                term = request.POST.get('term', '')
                products = Product.objects.filter(stock__gt=0)
                if term:
                    products = products.filter(Q(names__icontains=term) | Q(category__names__icontains=term) | Q(code__icontains=term))
                data = [product.toJSON() | {'value': product.names} for product in products.exclude(id__in=ids_exclude)[0:5]]
            elif action == 'get_products_data':
                ids_exclude = json.loads(request.POST['products_id'])
                # Capturar los datos del dataTable
                start = int(request.POST.get('start', 0))
                length = int(request.POST.get('length', 10))
                search = request.POST.get('search[value]', '')
                # Obtener nuesstro queryet
                products = Product.objects.filter(
                    stock__gt=0).exclude(id__in=ids_exclude)
                if search:
                    products = products.filter(names__icontains=search)
                # LLamamos a nuestro paginator
                paginator = Paginator(products, length)
                page_number = start // length + 1
                products_page = paginator.get_page(page_number)

                data = {
                    'data': [product.toJSON() for product in products_page],
                    'recordsTotal': paginator.count,
                    'recordsFiltered': paginator.count,
                    'draw': int(request.POST.get('draw', 1))
                }
            elif action == 'create_customer':
                customer = CustomerForm(request.POST)
                data = customer.save()
            else:
                data['error'] = 'No ha ingresado ninguna opción.'
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


class SaleDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Sale
    template_name = 'delete.html'
    permission_required = 'delete_sale'
    success_url = reverse_lazy('pos:sale_list')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(SaleDeleteView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'delete':
                with transaction.atomic():
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


class SaleInvoicePdfView(LoginRequiredMixin, ValidatePermissionRequiredMixin, View):
    permission_required = 'view_sale'

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('sale/invoice.html')
            context = {
                'sale': Sale.objects.get(pk=self.kwargs['pk']),
            }
            html = template.render(context)
            # css_url = os.path.join(settings.BASE_DIR, 'static/lib/adminlte-3.2.0/css/adminlte.min.css')
            pdf = HTML(string=html).write_pdf()
            return HttpResponse(pdf, content_type='application/pdf')
        except Exception as e:
            print(e)
        return HttpResponseRedirect(reverse_lazy('pos:sale_list'))
