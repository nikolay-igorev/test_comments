from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
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
    level = models.PositiveIntegerField()

    def __str__(self):
        return self.body
