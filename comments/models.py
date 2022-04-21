from django.contrib.auth import get_user_model
from django.db import models

from comments.managers import CommentManager
from posts.models import Post


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    body = models.CharField(max_length=140, verbose_name='Comment')
    created_at = models.DateTimeField(auto_now_add=True)
    # Родительский комментарий
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='parent_comment'
    )
    # Уровень вложенности
    nesting = models.PositiveIntegerField()

    objects = CommentManager()

    def __str__(self):
        return self.body


def list_to_queryset(queryset_list):
    queryset_pk = [comment.pk for comment in queryset_list]
    queryset = Comment.objects.filter(pk__in=queryset_pk)

    return queryset
