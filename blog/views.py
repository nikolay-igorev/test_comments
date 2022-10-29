from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.filters import OrderingFilter
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .models import Post, Comment
from .permissions import IsOwnerOrReadOnly, IsCommentOrPostOwnerOrReadOnly
from .serializers import PostSerializer, CommentSerializer

User = get_user_model()


class PostViewSet(viewsets.ModelViewSet):
	"""
    list: Список постов. Доступен всем пользователям
    create: Создание поста. Доступно авторизованным пользователям.
    retrieve: Просмотр поста. Доступен всем пользователям
    update: Изменение поста. Доступно владельцу поста.
    partial_update: Частичное изменение поста. Доступно владельцу поста.
    delete: Удаление поста. Доступно владельцу поста.
    """
	serializer_class = PostSerializer
	queryset = Post.objects.all()
	permission_classes = [IsOwnerOrReadOnly, ]
	filter_backends = (DjangoFilterBackend, OrderingFilter,)
	filterset_fields = ('user', 'created_at',)
	ordering_fields = ('title', 'created_at',)
	ordering = ('title',)

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
	"""
	list: Список комментариев. Доступен всем пользователям
	create: Создание комментария. Доступно авторизованным пользователям.
	retrieve: Просмотр комментария. Доступен всем пользователям
	update: Изменение комментария. Доступно владельцу комментария.
	partial_update: Частичное изменение комментария. Доступно владельцу комментария.
	delete: Удаление поста. Доступно владельцу комментария или поста.
	"""

	serializer_class = CommentSerializer
	queryset = Comment.objects.all()
	permission_classes = [IsOwnerOrReadOnly, ]
	filter_backends = (DjangoFilterBackend, OrderingFilter,)
	filterset_fields = ('user', 'post', 'created_at', 'parent')
	ordering_fields = ('created_at',)
	ordering = ('tree_id', 'lft')

	def get_permissions(self):
		if self.action == 'destroy':
			self.permission_classes = [IsCommentOrPostOwnerOrReadOnly]
		return super().get_permissions()

	def create(self, request, *args, **kwargs):
		raise NotFound()

	@action(["post"], detail=False)
	def create_post_comment(self, request, *args, **kwargs):
		post = get_object_or_404(Post, id=self.kwargs['post_id'])

		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save(
			user=self.request.user,
			post=post,
		)
		headers = self.get_success_headers(serializer.data)
		return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

	@action(["post"], detail=False)
	def create_child_comment(self, request, *args, **kwargs):
		parent = get_object_or_404(Comment, id=self.kwargs['comment_id'])

		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save(
			user=self.request.user,
			parent=parent
		)
		headers = self.get_success_headers(serializer.data)
		return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
