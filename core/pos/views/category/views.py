import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView

from core.pos.forms import CategoryForm
from core.pos.mixins import ValidatePermissionRequiredMixin
from core.pos.models import Category

import time

MODULE_NAME = 'Categoria'


class CategoryTemplateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, TemplateView):
    template_name = 'category/list.html'
    permission_required = 'view_category'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'get_categories':
                # Capturamos los datos mandados por dataTables
                start = int(request.POST.get('start', 0))
                length = int(request.POST.get('length', 10))
                term = request.POST.get('search[value]', '')
                # LLamos a nuestro queryset
                categories = Category.objects.all()
                # Si hay un dato a buscar lo filtramos
                if term:
                    categories = categories.filter(names__icontains=term)
                # Manejamos la paginacion con nuestro backend
                paginator = Paginator(categories, length)
                get_numbers = start // length + 1
                categories_page = paginator.get_page(get_numbers)
                # Vamoss a mandar toda nuestra información al dataTable
                data = {
                    'data': [category.toJSON() | {'position': position} for position, category in enumerate(categories_page, start=start + 1)],
                    'recordsTotal': paginator.count,
                    'recordsFiltered': paginator.count,
                    'draw': int(request.POST.get('draw', 1))
                }
            else:
                data['error'] = 'No ha ingresado ninguna opción.'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super(CategoryTemplateView, self).get_context_data(**kwargs)
        context['title'] = 'Listado de Categoria'
        context['entity'] = MODULE_NAME
        context['list_url'] = reverse_lazy('pos:category_list')
        context['create_url'] = reverse_lazy('pos:category_create')
        return context


class CategoryCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category/create.html'
    success_url = reverse_lazy('pos:category_list')
    permission_required = 'add_category'
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
        context = super(CategoryCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Creación de categoria'
        context['entity'] = MODULE_NAME
        context['action'] = 'create'
        context['list_url'] = self.success_url
        return context


class CategoryUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category/create.html'
    success_url = reverse_lazy('pos:category_list')
    permission_required = 'change_category'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(CategoryUpdateView, self).dispatch(request, *args, **kwargs)

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
        context = super(CategoryUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Actualización de un producto'
        context['entity'] = MODULE_NAME
        context['action'] = 'update'
        context['list_url'] = self.success_url
        return context


class CategoryDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Category
    template_name = 'delete.html'
    success_url = reverse_lazy('pos:category_list')
    permission_required = 'delete_category'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(CategoryDeleteView, self).dispatch(request, *args, **kwargs)

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
        context = super(CategoryDeleteView, self).get_context_data(**kwargs)
        context['title'] = 'Eliminación de Categoria'
        context['entity'] = MODULE_NAME
        context['action'] = "delete"
        context['list_url'] = self.success_url
        return context
