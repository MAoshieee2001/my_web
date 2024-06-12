from django.forms import *

from core.accounts.models import User


class UserForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['autofocus'] = True

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                password = self.cleaned_data.get('password', '')  # Obtenemos la contraseña del campo del formulario
                instance = super().save(commit=False)  # Instanciamos el objeto, sin guardar dado quue puede presentarse un cambio
                if instance.pk is None or User.objects.get(pk=instance.pk).password != password:  # Validamos si el usuario es nuevo o hubo un cambio de contraseña
                    instance.set_password(password)  # Seteamos la contrasseña
                instance.save()  # Guardamoss los cambios del usuario
                instance.groups.clear()  # Limpiamos el grupo
                instance.groups.set(self.cleaned_data['groups'])  # Seteamos el nuevo grupo
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'email', 'groups', 'imagen']
        exclude = ['last_login', 'date_joined', 'user_permissions', 'is_staff', 'is_active', 'is_superuser']
        widgets = {
            'first_name': TextInput(attrs={
                'placeholder': 'Ingrese el nombre del usuario.',
            }),
            'last_name': TextInput(attrs={
                'placeholder': 'Ingrese el apellido del usuario.',
            }),
            'username': TextInput(attrs={
                'placeholder': 'Ingrese el username del usuario.',
            }),
            'password': PasswordInput(render_value=True, attrs={
                'placeholder': 'Ingrese el password del usuario.',
            }),
            'email': TextInput(attrs={
                'placeholder': 'Ingrese el email del usuario.',
            }),
            'groups': SelectMultiple(attrs={
            }),
        }


class UserProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['autofocus'] = True

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                self.instance.save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'imagen']
        exclude = ['last_login', 'date_joined', 'user_permissions', 'is_staff', 'is_active', 'is_superuser', 'password']
        widgets = {
            'first_name': TextInput(attrs={
                'placeholder': 'Ingrese el nombre del usuario.',
            }),
            'last_name': TextInput(attrs={
                'placeholder': 'Ingrese el apellido del usuario.',
            }),
            'username': TextInput(attrs={
                'placeholder': 'Ingrese el username del usuario.',
            }),
            'email': TextInput(attrs={
                'placeholder': 'Ingrese el email del usuario.',
            }),
        }
