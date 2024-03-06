from crum import get_current_request
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import model_to_dict

import settings


class User(AbstractUser):
    imagen = models.ImageField(upload_to='customers/', null=True, blank=True, verbose_name='Imagen')

    def get_imagen(self):
        return f'{settings.MEDIA_URL}{self.imagen}' if self.imagen else f'{settings.STATIC_URL}img/empty.png'

    def get_full_name(self):
        return f'{self.last_name}, {self.first_name}'

    def toJSON(self):
        item = model_to_dict(self, exclude=['password', 'is_superuser', 'is_staff', 'is_active', 'user_permissions'])
        item['last_login'] = self.last_login.strftime('%Y-%m-%d') if self.last_login else None
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['imagen'] = self.get_imagen()
        item['full_names'] = self.get_full_name()
        item['groups'] = [{'id': group.id, 'names': group.name} for group in self.groups.all()]
        return item

    def set_group_session(self):
        request = get_current_request()
        group = self.groups.first()
        if group is not None:
            if 'group' not in request.session or request.session['group'] is None:
                request.session['group'] = {'id': group.id, 'names': group.name}
            elif 'group' in request.session and not self.groups.all().filter(pk=request.session['group']['id']).exists():
                request.session['group'] = {'id': group.id, 'names': group.name}
        else:
            request.session['group'] = None

    class Meta:
        db_table = 'user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['id']
