from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from core.dashboard.views import DashboardTemplateView

urlpatterns = [
    path('', include('core.login.urls')),
    path('admin/', admin.site.urls),
    path('core/', include('core.pos.urls')),
    path('accounts/', include('core.accounts.urls')),
    path('reports/', include('core.reports.urls')),
    path('dashboard/', DashboardTemplateView.as_view(), name='dashboard'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

