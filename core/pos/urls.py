from django.urls import path

from core.pos.views.category.views import *
from core.pos.views.company.views import CompanyUpdateView
from core.pos.views.customer.views import *
from core.pos.views.log.views import LogTemplateView
from core.pos.views.product.views import *
from core.pos.views.sale.views import *

app_name = 'pos'

urlpatterns = [
    # ! Category
    path('category/', CategoryTemplateView.as_view(), name='category_list'),
    path('category/create/', CategoryCreateView.as_view(), name='category_create'),
    path('category/update/<int:pk>/', CategoryUpdateView.as_view(), name='category_update'),
    path('category/delete/<int:pk>/', CategoryDeleteView.as_view(), name='category_delete'),
    # ! Product
    path('product/', ProductTemplateView.as_view(), name='product_list'),
    path('product/create/', ProductCreateView.as_view(), name='product_create'),
    path('product/update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
    # ! Customer
    path('customer/', CustomerTemplateView.as_view(), name='customer_list'),
    path('customer/create/', CustomerCreateView.as_view(), name='customer_create'),
    path('customer/update/<int:pk>/', CustomerUpdateView.as_view(), name='customer_update'),
    path('customer/delete/<int:pk>/', CustomerDeleteView.as_view(), name='customer_delete'),
    # ! SALE
    path('sale/', SaleTemplateView.as_view(), name='sale_list'),
    path('sale/create/', SaleCreateView.as_view(), name='sale_create'),
    path('sale/delete/<int:pk>/', SaleDeleteView.as_view(), name='sale_delete'),
    path('sale/invoice/pdf/<int:pk>/', SaleInvoicePdfView.as_view(), name='sale_invoice_pdf'),
    # ! LOG
    path('log/', LogTemplateView.as_view(), name='log_list'),
    # ! Company
    path('company/', CompanyUpdateView.as_view(), name='company_update'),

]
