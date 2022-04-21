from django.urls import path

import comments.views as views

urlpatterns = [
    # Полный список комментариев
    path('comments/', views.CommentsListView.as_view(), name='comments_list'),
    # Список комментариев к посту до 3 уровня вложенности
    path('post/<int:pk>/comments/', views.CommentsPostListView.as_view(), name='comments_post_list'),
    # Список комментариев к посту
    path('post/<int:pk>/comments/all', views.CommentsPostListView.as_view(), name='comments_post_all_list'),
    # Список ответов к комментарию до 3 уровня вложенности
    path('comments/<int:pk>/', views.CommentsRepliesListView.as_view(), name='comment_replies_list'),
    # Список ответов к комментарию
    path('comments/<int:pk>/all', views.CommentsRepliesListView.as_view(), name='comment_replies_all_list'),
    # Создание комментария
    path('post/<int:pk>/comments/create/', views.CommentCreateView.as_view(), name='comment_create'),
    # Создание ответа к комментарию
    path('comments/<int:pk>/create/', views.CommentReplyCreateView.as_view(), name='comment_reply_create'),
]
