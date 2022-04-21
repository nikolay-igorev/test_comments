from django.urls import path

import posts.views as views

urlpatterns = [
    path('', views.PostUserListView.as_view(), name='posts_list'),
    path('<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('create/', views.PostCreateView.as_view(), name='post_create'),
    path('<int:pk>/edit', views.PostUpdateView.as_view(), name='post_update'),
    path('<int:pk>/delete', views.PostDeleteView.as_view(), name='post_delete'),
]
