import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView

from core.pos.forms import CustomerForm
from core.pos.mixins import ValidatePermissionRequiredMixin
from core.pos.models import Customer

MODULE_NAME = 'Categoria'


class CustomerTemplateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, TemplateView):
    template_name = 'customer/list.html'
    permission_required = 'view_customer'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'get_customers':
                customers = Customer.objects.all()
                data = [customer.toJSON() | {'position': position} for position, customer in enumerate(customers, start=1)]
            else:
                data['error'] = 'No ha ingresado ninguna opción.'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super(CustomerTemplateView, self).get_context_data(**kwargs)
        context['title'] = 'Listado de Clientes'
        context['entity'] = MODULE_NAME
        context['list_url'] = reverse_lazy('pos:customer_list')
        context['create_url'] = reverse_lazy('pos:customer_create')
        return context


class CustomerCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'customer/create.html'
    success_url = reverse_lazy('pos:customer_list')
    permission_required = 'add_customer'
    url_redirect = success_url

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'create':
                data = self.get_form().save()
            else:
                data['error'] = 'No ha ingresado ninguna opción.'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super(CustomerCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Creación de Cliente'
        context['entity'] = MODULE_NAME
        context['action'] = 'create'
        context['list_url'] = self.success_url
        return context


class CustomerUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'customer/create.html'
    success_url = reverse_lazy('pos:customer_list')
    permission_required = 'change_customer'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(CustomerUpdateView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'update':
                data = self.get_form().save()
            else:
                data['error'] = 'No ha ingresado ninguna opción.'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super(CustomerUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Edicción de Cliente'
        context['entity'] = MODULE_NAME
        context['action'] = 'update'
        context['list_url'] = self.success_url
        return context


class CustomerDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Customer
    template_name = 'delete.html'
    success_url = reverse_lazy('pos:customer_list')
    permission_required = 'delete_customer'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(CustomerDeleteView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'delete':
                self.object.delete()
            else:
                data['error'] = 'No ha ingresado ninguna opción.'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super(CustomerDeleteView, self).get_context_data(**kwargs)
        context['title'] = 'Eliminación de Cliente'
        context['entity'] = MODULE_NAME
        context['action'] = 'delete'
        context['list_url'] = self.success_url
        return context
