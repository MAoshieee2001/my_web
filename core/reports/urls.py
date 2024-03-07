from django.urls import path

from core.reports.views.sale.views import ReportSaleTemplateView

app_name = 'reports'

urlpatterns = [
    path('sale/', ReportSaleTemplateView.as_view(), name='sale_report'),

]
