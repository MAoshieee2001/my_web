from django.forms import *

from core.pos.models import *


class CategoryForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['names'].widget.attrs['autofocus'] = True

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
        model = Category
        fields = '__all__'
        widgets = {
            'names': TextInput(attrs={
                'placeholder': 'Ingrese el nombre de la categoria.',
            }),
            'description': Textarea(attrs={
                'placeholder': 'Ingrese la descripción de la categoria.',
                'rows': 4,
                'style': 'resize:none',
            })
        }


class ProductForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['category'].widget.attrs['autofocus'] = True
        self.fields['category'].queryset = Category.objects.none()

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

    def clean(self):
        cleaned_data = super(ProductForm, self).clean()
        pvp = float(cleaned_data['pvp'])
        if pvp <= 0.00:
            raise ValidationError('El precio de la venta debe ser superior a 0.00')
        return cleaned_data

    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'code': TextInput(attrs={
                'placeholder': 'Ingrese el código del producto.',
            }),
            'names': TextInput(attrs={
                'placeholder': 'Ingrese el nombre del producto.',
            }),
            'description': Textarea(attrs={
                'placeholder': 'Ingrese la descripción del producto.',
                'rows': 4,
                'style': 'resize:none;',
            }),
            'pvp': TextInput(attrs={
                'placeholder': 'Ingrese el precio de venta del producto.',
            }),
            'stock': TextInput(attrs={
                'placeholder': 'Ingrese el stock actual del producto.',
            }),

        }


class CustomerForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        self.fields['first_names'].widget.attrs['autofocus'] = True

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                instance = super().save()
                data = instance.toJSON()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data

    class Meta:
        model = Customer
        fields = '__all__'
        widgets = {
            'first_names': TextInput(attrs={
                'placeholder': 'Ingrese el nombre completo del cliente.',
            }),
            'last_names': TextInput(attrs={
                'placeholder': 'Ingrese el apellido completo del cliente.',
            }),
            'date_birthday': DateInput(format='%Y-%m-%d', attrs={
                'placeholder': 'Ingrese la fecha de nacimiento del cliente.',
                'class': 'datetimepicker-input',
                'data-target': 'id_date_birthday',
                'data-toggle': 'datetimepicker',
            }),
            'dni': TextInput(attrs={
                'placeholder': 'Ingrese el dni del cliente.',
            }),
            'address': TextInput(attrs={
                'placeholder': 'Ingrese la dirección del cliente.',
            }),
            'phone': TextInput(attrs={
                'placeholder': 'Ingrese el celular del cliente.',
            }),
        }


class SaleForm(ModelForm):
    def __init__(self, **kwargs):
        super(SaleForm, self).__init__(**kwargs)
        self.fields['customer'].queryset = Customer.objects.none()

    class Meta:
        model = Sale
        fields = '__all__'
        widgets = {
            'iva': TextInput(attrs={
                'placeholder': 'Digite el IVA',
            }),
            'cash': TextInput(attrs={
                'placeholder': 'Digite el efectivo a pagar',
            }),
        }


class CompanyForm(ModelForm):
    def __init__(self, **kwargs):
        super(CompanyForm, self).__init__(**kwargs)

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
        model = Company
        fields = '__all__'
        widgets = {
            'names': TextInput(attrs={
                'placeholder': 'Ingrese la razón social de su empresa.',
            }),
            'ruc': TextInput(attrs={
                'placeholder': 'Ingrese el RUC de su empresa.',
            }),
            'address': Textarea(attrs={
                'placeholder': 'Ingrese la dirección matriz de su empresa.',
            }),
            'phone': TextInput(attrs={
                'placeholder': 'Ingrese el celular de su empresa.',
            }),
            'email': EmailInput(attrs={
                'placeholder': 'Ingrese el email de su empresa.',
            }),
        }
