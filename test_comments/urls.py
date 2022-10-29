from django.contrib import admin
from django.urls import path, include
from .yasg import urlpatterns as yasg_urls

urlpatterns = [
	path('admin/', admin.site.urls),
	path('api/v1/', include('blog.urls')),
	path('api/v1/', include('accounts.urls')),

	# path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
	path('auth/', include('djoser.urls.authtoken')),
	path('auth/', include('djoser.urls.jwt')),
]

urlpatterns += yasg_urls
