
from django.contrib import admin
from django.urls import path, include

admin.site.site_header = " Admin"
admin.site.site_title = " Admin Portal"
admin.site.index_title = "Welcome to Admin Dashboard"

from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import RedirectView

urlpatterns = [
    path('favicon.ico', RedirectView.as_view(url='/static/path/to/favicon.ico', permanent=True)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/',include('api.urls')),
    path('user/', include('account.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)