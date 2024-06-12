from django.contrib import messages
from django.contrib.auth.models import Group
from django.shortcuts import redirect
from django.urls import reverse_lazy

import settings
from core.pos.models import Company


class ValidatePermissionRequiredMixin:  # Clase Mixin, que permitira poder validar el tema de los permisos a mi vista
    permission_required = ''
    url_redirect = None

    def get_perms(self):  # Permite obtener si se esta mandado una tupla o string, del tema de los permisos
        if isinstance(self.permission_required, str):
            perms = (self.permission_required,)
        else:
            perms = self.permission_required
        return perms

    def get_url_redirect(self):  # Permite obtener la ruta, que sera posteriormente utilizado
        return self.url_redirect if self.url_redirect else settings.LOGIN_REDIRECT_URL

    def get(self, request, *args, **kwargs):  # Permite validar toda la funcionalidadd del tema de los permisos
        request.user.set_group_session()
        if request.session['group'] is not None:
            group = Group.objects.get(pk=request.session['group']['id'])
            if group.permissions.filter(codename=self.permission_required).exists():
                return super().get(request, *args, **kwargs)
        messages.error(request, 'Usted no tiene los permisos necesarios para ingresar al siguinte módulo.')
        return redirect(self.get_url_redirect())


class CompanyIsExistMixin:  # Clase Mixin, que permite validar si existe una compañia antess de poder ingresar a la vista de venta
    def get(self, request, *args, **kwargs):
        company = Company.objects.first()
        if company:
            super(CompanyIsExistMixin, self).get(request, *args, **kwargs)
        messages.error(request, 'Debe de existir su compañia para poder hacer ventas, pongase contacto con el administrador.')
        return redirect(reverse_lazy('pos:company_update'))
