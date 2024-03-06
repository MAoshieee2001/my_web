from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

import settings
from core.dashboard.views import DashboardTemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('core/', include('core.pos.urls')),
    path('accounts/', include('core.accounts.urls')),
    path('', include('core.login.urls')),
    path('dashboard/', DashboardTemplateView.as_view(), name='dashboard'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
