from django.contrib import admin
from django.urls import path, include

# from api.urls import posts_router, comments_router
from api.urls import blog_router

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include((blog_router.urls, 'books'))),
]
