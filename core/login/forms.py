from django import forms
from django.contrib.auth import authenticate

from core.accounts.models import User


class AuthenticationForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
    }))

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username', '')
        password = cleaned_data.get('password', '')
        if len(username) == 0:
            raise forms.ValidationError('Debe de ingresar el usuario.')
        if len(password) == 0:
            raise forms.ValidationError('Debe de ingresar la contraseña.')
        user = authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError(
                'Por favor introduzca el nombre de usuario y la clave correctos para una cuenta de personal.'
                ' Observe que ambos campos pueden ser sensibles a mayúsculas.')
        return cleaned_data

    def get_user(self):
        username = self.cleaned_data.get('username', '')
        return User.objects.get(username=username)
