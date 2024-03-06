import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView

from core.pos.forms import ProductForm
from core.pos.mixins import ValidatePermissionRequiredMixin
from core.pos.models import Product, Category

MODULE_NAME = 'Producto'


class ProductTemplateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, TemplateView):
    template_name = 'product/list.html'
    permission_required = 'view_product'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'get_products':
                products = Product.objects.all()
                data = [product.toJSON() | {'position': position} for position, product in enumerate(products, start=1)]
            else:
                data['error'] = 'No ha ingresado ninguna opción.'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super(ProductTemplateView, self).get_context_data(**kwargs)
        context['title'] = 'Listado de Producto'
        context['entity'] = MODULE_NAME
        context['list_url'] = reverse_lazy('pos:product_list')
        context['create_url'] = reverse_lazy('pos:product_create')
        return context


class ProductCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/create.html'
    success_url = reverse_lazy('pos:product_list')
    permission_required = 'add_product'
    url_redirect = success_url

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'get_categories_term':
                term = request.POST.get('term', '')
                categories = Category.objects.all()
                if term:
                    categories = categories.filter(names__icontains=term)
                data = [{'id': category.id, 'text': category.names} for category in categories[0:10]]
            elif action == 'create':
                form = self.get_form()
                form.fields['category'].queryset = Category.objects.filter(pk=request.POST['category'])
                data = form.save()
            else:
                data['error'] = 'No ha ingresado ninguna opción.'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super(ProductCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Creación de Producto'
        context['entity'] = MODULE_NAME
        context['action'] = 'create'
        context['list_url'] = self.success_url
        return context


class ProductUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/create.html'
    success_url = reverse_lazy('pos:product_list')
    permission_required = 'change_product'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(ProductUpdateView, self).dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = super(ProductUpdateView, self).get_form(form_class)
        form.fields['category'].queryset = Category.objects.filter(pk=self.object.category.pk)
        return form

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'get_categories_term':
                term = request.POST.get('term', '')
                categories = Category.objects.all()
                if term:
                    categories = categories.filter(names__icontains=term)
                data = [{'id': category.id, 'text': category.names} for category in categories[0:10]]
            elif action == 'update':
                form = self.get_form()
                form.fields['category'].queryset = Category.objects.filter(pk=request.POST['category'])
                data = form.save()
            else:
                data['error'] = 'No ha ingresado ninguna opción.'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json ')

    def get_context_data(self, **kwargs):
        context = super(ProductUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Actualización de Producto'
        context['entity'] = MODULE_NAME
        context['action'] = 'update'
        context['list_url'] = self.success_url
        return context


class ProductDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Product
    template_name = 'delete.html'
    success_url = reverse_lazy('pos:product_list')
    permission_required = 'delete_product'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(ProductDeleteView, self).dispatch(request, *args, **kwargs)

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
        context = super(ProductDeleteView, self).get_context_data(**kwargs)
        context['title'] = 'Eliminación de Producto'
        context['entity'] = MODULE_NAME
        context['action'] = 'delete'
        context['list_url'] = self.success_url
        return context
