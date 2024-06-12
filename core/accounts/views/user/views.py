import json

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, FormView

import settings
from core.accounts.forms import UserForm, UserProfileForm
from core.accounts.models import User
from core.pos.mixins import ValidatePermissionRequiredMixin

MODULE_NAME = 'Usuario'


class UserTemplateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, TemplateView):  # Clase que permite listar los usuarios
    template_name = 'user/list.html'
    permission_required = 'view_user'

    def post(self, request, *args, **kwargs):  # Funcion que permite realizar acciones mediante el POST
        data = {}
        try:
            action = request.POST['action']
            if action == 'get_users':
                users = User.objects.all()
                data = [user.toJSON() | {'position': position} for position, user in enumerate(users, start=1)]
            else:
                data['error'] = 'No ha ingresado ninguna opción.'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):  # Devolvemos un diccionario que debe de cargar en el aplicativo web
        context = super(UserTemplateView, self).get_context_data(**kwargs)
        context['title'] = 'Listado de Usuarios'
        context['entity'] = MODULE_NAME
        context['list_url'] = reverse_lazy('accounts:user_list')
        context['create_url'] = reverse_lazy('accounts:user_create')
        return context


class UserCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):  # Vista que permite crear un usuario
    model = User
    form_class = UserForm
    template_name = 'user/create.html'
    success_url = reverse_lazy('accounts:user_list')
    permission_required = 'add_user'
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
        context = super(UserCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Creación de Usuario'
        context['entity'] = MODULE_NAME
        context['action'] = 'create'
        context['list_url'] = self.success_url
        return context


class UserUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):  # Vista que permite actualizar el usuario
    model = User
    form_class = UserForm
    template_name = 'user/create.html'
    success_url = reverse_lazy('accounts:user_list')
    permission_required = 'change_user'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(UserUpdateView, self).dispatch(request, *args, **kwargs)

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
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Edicción de Usuario'
        context['entity'] = MODULE_NAME
        context['action'] = 'update'
        context['list_url'] = self.success_url
        return context


class UserDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):  # Vista que permite eliminar el usuario
    model = User
    template_name = 'delete.html'
    success_url = reverse_lazy('pos:customer_list')
    permission_required = 'delete_user'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(UserDeleteView, self).dispatch(request, *args, **kwargs)

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
        context = super(UserDeleteView, self).get_context_data(**kwargs)
        context['title'] = 'Eliminación de Usuario'
        context['entity'] = MODULE_NAME
        context['action'] = 'delete'
        context['list_url'] = self.success_url
        return context


class UserProfileView(LoginRequiredMixin, UpdateView):  # Vista que permite visualizar el perfil de usuario
    model = User
    form_class = UserProfileForm
    template_name = 'user/create.html'
    success_url = reverse_lazy('dashboard')

    def get_object(self, queryset=None):
        return self.request.user

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(UserProfileView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'update_profile':
                data = self.get_form().save()
            else:
                data['error'] = 'No ha ingresado ninguna opción.'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        context['title'] = 'Mi Perfil'
        context['entity'] = MODULE_NAME
        context['action'] = 'update_profile'
        context['list_url'] = self.success_url
        return context


class UserChangePassswordView(LoginRequiredMixin, FormView):  # Vista que permite cambiar la contraseña del usuario
    form_class = PasswordChangeForm
    template_name = 'user/create.html'
    success_url = reverse_lazy('dashboard')

    def get_form(self, form_class=None):
        form = PasswordChangeForm(user=self.request.user)
        for i in form:
            i.field.widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off',
                'placeholder': f'Ingrese su {i.label.lower()}'
            })
        return form

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'update_password':
                form = PasswordChangeForm(user=request.user, data=request.POST)
                if form.is_valid():
                    form.save()
                    update_session_auth_hash(request, form.user)
                else:
                    data['error'] = form.errors
            else:
                data['error'] = 'No ha ingresado ninguna opción.'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super(UserChangePassswordView, self).get_context_data(**kwargs)
        context['title'] = 'Actualizar contraseña'
        context['entity'] = MODULE_NAME
        context['list_url'] = self.success_url
        context['action'] = 'update_password'
        return context


class UserChangeGroupView(LoginRequiredMixin, View):  # Vista que permite cambiar los grupos del usuario

    def get(self, request, *args, **kwargs):
        try:
            group = Group.objects.get(pk=self.kwargs['pk'])
            request.session['group'] = {'id': group.id, 'names': group.name}
        except Exception as e:
            request.session['group'] = None
        return redirect(settings.LOGIN_REDIRECT_URL)
