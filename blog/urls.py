from django.urls import path

from . import views
from rest_framework.routers import DefaultRouter

urlpatterns = [
	path('posts/<int:post_id>/comments/', views.CommentViewSet.as_view({'post': 'create_post_comment'}),
	     name='comment-post-create'),
	path('comments/<int:comment_id>/comments/', views.CommentViewSet.as_view({'post': 'create_child_comment'}),
	     name='comment-child-create'),
]

router = DefaultRouter()

router.register("posts", views.PostViewSet)
router.register("comments", views.CommentViewSet)

urlpatterns += router.urls
