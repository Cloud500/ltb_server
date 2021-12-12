from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('homepage.urls', namespace='homepage')),
    path('tlb_management/', admin.site.urls),
    path('ltb/', include('ltb.urls', namespace='ltb')),
    path('stock/', include('stock.urls', namespace='stock')),
    path('api/v1/', include('api.urls', namespace='api'))
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
