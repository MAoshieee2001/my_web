from django.contrib import messages
from django.contrib.auth.models import Group
from django.shortcuts import redirect

import settings


class ValidatePermissionRequiredMixin:
    permission_required = ''
    url_redirect = None

    def get_perms(self):
        if isinstance(self.permission_required, str):
            perms = (self.permission_required,)
        else:
            perms = self.permission_required
        return perms

    def get_url_redirect(self):
        return self.url_redirect if self.url_redirect else settings.LOGIN_REDIRECT_URL

    def get(self, request, *args, **kwargs):
        request.user.set_group_session()
        if request.session['group'] is not None:
            group = Group.objects.get(pk=request.session['group']['id'])
            if group.permissions.filter(codename=self.permission_required).exists():
                return super().get(request, *args, **kwargs)
        messages.error(request, 'Usted no tiene los permisos necesarios para ingresar al siguinte módulo.')
        return redirect(self.get_url_redirect())
