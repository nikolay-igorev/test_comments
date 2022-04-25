from rest_framework.viewsets import ModelViewSet

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
