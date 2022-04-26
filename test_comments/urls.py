from django.contrib import admin
from django.urls import path, include
from .yasg import urlpatterns as yasg_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls')),
]

urlpatterns += yasg_urls
