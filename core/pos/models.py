from datetime import datetime
from django.db import models
from django.db.models import Sum, FloatField
from django.db.models.functions import Coalesce
from django.forms import model_to_dict

import settings
from core.accounts.models import User
from core.pos.choices import choices_gender, choices_action


class Category(models.Model):
    names = models.CharField(max_length=144, unique=True, verbose_name='Nombre')
    description = models.TextField(blank=True, null=True, verbose_name='Descripción')

    def __str__(self):
        return self.names

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        db_table = 'categoria'
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['id']


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Categoria')
    code = models.CharField(max_length=20,  verbose_name='Código')
    names = models.CharField(max_length=144, verbose_name='Nombre')
    description = models.TextField(blank=True, null=True, verbose_name='Descripción')
    pvp = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Precio de venta')
    stock = models.PositiveIntegerField(default=0, verbose_name='Stock')
    imagen = models.ImageField(upload_to='products/', null=True, blank=True, verbose_name='Imagen')

    def __str__(self):
        return self.names

    def get_short_names(self):
        return f'{self.category.names} {self.names}'

    def get_long_names(self):
        return f'{self.category.names} {self.names} - Código : {self.code}'

    def get_imagen(self):
        return f'{settings.MEDIA_URL}{self.imagen}' if self.imagen else f'{settings.STATIC_URL}img/empty.png'

    def toJSON(self):
        item = model_to_dict(self)
        item['category'] = self.category.toJSON()
        item['pvp'] = float(self.pvp)
        item['imagen'] = self.get_imagen()
        item['short_names'] = self.get_short_names()
        item['long_names'] = self.get_long_names()
        return item

    class Meta:
        db_table = 'producto'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['id']


######################################################################################################################
class Customer(models.Model):
    first_names = models.CharField(max_length=144, verbose_name='Nombre Completo')
    last_names = models.CharField(max_length=144, verbose_name='Apellido completo')
    date_birthday = models.DateField(default=datetime.now, verbose_name='Fecha de nacimiento')
    gender = models.BooleanField(default=True, choices=choices_gender, verbose_name='Género')
    dni = models.CharField(max_length=8, unique=True, verbose_name='DNI')
    address = models.CharField(max_length=240, null=True, blank=True, verbose_name='Dirección')
    phone = models.CharField(max_length=9, null=True, blank=True, verbose_name='Telefono celular')

    def __str__(self):
        return f'{self.last_names}, {self.first_names}'

    def get_full_names(self):
        return f'{self.last_names}, {self.first_names}'

    def get_full_names_DNI(self):
        return f'{self.last_names}, {self.first_names} - DNI : {self.dni}'

    def toJSON(self):
        item = model_to_dict(self)
        item['date_birthday'] = self.date_birthday.strftime('%d-%m-%Y')
        item['gender'] = {'id': self.gender, 'names': self.get_gender_display()}
        item['full_names'] = self.get_full_names()
        item['full_names_DNI'] = self.get_full_names_DNI()
        return item

    class Meta:
        db_table = 'cliente'
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['id']


class Sale(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, verbose_name='Cliente')
    employee = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Empleado')
    date_joined = models.DateField(default=datetime.now, verbose_name='Fecha Registro')
    subtotal = models.DecimalField(default=0.00, decimal_places=2, max_digits=9, verbose_name='Subtotal')
    iva = models.DecimalField(default=0.00, decimal_places=2, max_digits=9, verbose_name='IVA')
    total = models.DecimalField(default=0.00, decimal_places=2, max_digits=9, verbose_name='Total')
    cash = models.DecimalField(default=0.00, decimal_places=2, max_digits=9, verbose_name='Efectivo')
    change = models.DecimalField(default=0.00, decimal_places=2, max_digits=9, verbose_name='Cambio')

    def __str__(self):
        return self.customer.get_full_names()

    def calcule_invoice(self):
        self.subtotal = self.detailsale_set.aggregate(result=Sum(Coalesce('subtotal', 0.00, output_field=FloatField()))).get('result')
        self.total = self.subtotal + (self.subtotal * self.iva)
        self.change = self.cash - self.total
        self.save()

    def toJSON(self):
        item = model_to_dict(self)
        item['customer'] = self.customer.toJSON()
        item['employee'] = self.employee.toJSON()
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['subtotal'] = float(self.subtotal)
        item['iva'] = float(self.iva)
        item['total'] = float(self.total)
        item['cash'] = float(self.cash)
        item['change'] = float(self.change)
        return item

    class Meta:
        db_table = 'venta'
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        ordering = ['id']


class DetailSale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name='Producto')
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, verbose_name='Venta')
    quantity = models.IntegerField(default=0, verbose_name='Cantidad')
    price = models.DecimalField(default=0.00, decimal_places=2, max_digits=9, verbose_name='Precio')
    subtotal = models.DecimalField(default=0.00, decimal_places=2, max_digits=9, verbose_name='Subtotal')

    def __str__(self):
        return self.product.names

    def toJSON(self):
        item = model_to_dict(self, exclude=['sale'])
        item['product'] = self.product.toJSON()
        item['price'] = float(self.price)
        item['subtotal'] = float(self.subtotal)
        return item

    class Meta:
        db_table = 'detalle_venta'
        verbose_name = 'Detalle Venta'
        verbose_name_plural = 'Detalle Ventas'
        ordering = ['id']


######################################################################################################################
class Logs(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, verbose_name='Cliente')
    employee = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Empleado', related_name='employee_logs')
    date_joined = models.DateField(default=datetime.now, verbose_name='Fecha Registro')
    subtotal = models.DecimalField(default=0.00, decimal_places=2, max_digits=9, verbose_name='Subtotal')
    iva = models.DecimalField(default=0.00, decimal_places=2, max_digits=9, verbose_name='IVA')
    total = models.DecimalField(default=0.00, decimal_places=2, max_digits=9, verbose_name='Total')
    cash = models.DecimalField(default=0.00, decimal_places=2, max_digits=9, verbose_name='Efectivo')
    change = models.DecimalField(default=0.00, decimal_places=2, max_digits=9, verbose_name='Cambio')
    date_log = models.DateField(default=datetime.now, verbose_name='Fecha Actualización')
    user_log = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Ussuario', related_name='user_logs')
    action = models.CharField(max_length=10, choices=choices_action, verbose_name='Acción')

    def __str__(self):
        return f'Acción : {self.action} - Usuario : {self.user_log}'

    def toJSON(self):
        item = model_to_dict(self, exclude=['subtotal', 'iva', 'cash', 'change'])
        item['customer'] = self.customer.toJSON()
        item['employee'] = self.employee.toJSON()
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['total'] = float(self.total)
        item['user_log'] = self.user_log.toJSON()
        item['date_log'] = self.date_log.strftime('%Y-%m-%d')
        item['action'] = {'id': self.action, 'names': self.get_action_display()}
        return item

    class Meta:
        db_table = 'bitacora'
        verbose_name = 'Bitacora'
        verbose_name_plural = 'Bitacoras'
        ordering = ['id']
