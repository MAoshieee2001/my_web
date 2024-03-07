from django import forms


class ReportSaleForm(forms.Form):
    date_range = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Ingrese el rango de fecha para el filtrado.',
    }), label='Rango de Fecha')
