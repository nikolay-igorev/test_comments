from rest_framework.generics import ListAPIView, ListCreateAPIView, get_object_or_404

from .models import Post, Comment
from .serializers import PostSerializer, CommentListSerializer, CommentCreateSerializer


class PostListCreateAPIView(ListCreateAPIView):
    """
    get: Список постов
    post: Создание поста
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CommentListAPIView(ListAPIView):
    """
    get: Полный список комментариев к посту в древовидном порядке
    """
    serializer_class = CommentListSerializer
    queryset = Comment.objects.all()


class CommentPostListCreateAPIView(ListCreateAPIView):
    """
    get: Список комментариев к посту до 3 уровня вложенности
    post: Создание комментария к посту
    """
    serializer_class = CommentListSerializer

    def get_queryset(self):
        max_level = 2
        return Comment.objects.filter(post_id=self.kwargs['post_id'], level__lte=max_level)

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.request.method == 'POST':
            serializer_class = CommentCreateSerializer

        return serializer_class

    def perform_create(self, serializer):
        serializer.validated_data['post'] = get_object_or_404(Post, id=self.kwargs['post_id'])
        serializer.save()


class CommentReplyListCreateAPIView(ListCreateAPIView):
    """
    get: Список ответов на комментарий до 3 уровня вложенности
    post: Создание ответа на комментарий
    """
    serializer_class = CommentListSerializer

    def get_queryset(self):
        comment = Comment.objects.get(id=self.kwargs['comment_id'])
        level = comment.level
        max_level = level + 3

        queryset = comment.get_descendants().filter(level__lte=max_level)

        return queryset

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.request.method == 'POST':
            serializer_class = CommentCreateSerializer

        return serializer_class

    def perform_create(self, serializer):
        serializer.validated_data['parent'] = get_object_or_404(Comment, id=self.kwargs['comment_id'])
        serializer.validated_data['post'] = get_object_or_404(Post, comment=self.kwargs['comment_id'])

        serializer.save()
