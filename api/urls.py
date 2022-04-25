from rest_framework import routers

from .views import PostViewSet, CommentViewSet

blog_router = routers.SimpleRouter()
blog_router.register(r'posts', PostViewSet)
blog_router.register(r'comments', CommentViewSet)
