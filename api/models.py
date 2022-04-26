from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Post(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(MPTTModel):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comment'
    )
    body = models.TextField(verbose_name='Comment')
    created_at = models.DateTimeField(auto_now_add=True)
    parent = TreeForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children_comment',
        on_delete=models.CASCADE
    )

    class MPTTMeta:
        order_insertion_by = ['created_at']

    class Meta:
        ordering = ['tree_id', 'lft']

    def __str__(self):
        return self.body
