from django.urls import path

import api.views as views


urlpatterns = [
    path('posts/', views.PostListCreateAPIView.as_view()),
    path('posts/<int:post_id>/', views.CommentPostListCreateAPIView.as_view()),
    path('comments/', views.CommentListAPIView.as_view()),
    path('comments/<int:comment_id>', views.CommentReplyListCreateAPIView.as_view()),
]
