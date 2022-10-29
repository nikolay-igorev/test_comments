from django.contrib.auth import get_user_model
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

User = get_user_model()


class Post(models.Model):
	user = models.ForeignKey(User, related_name='post', on_delete=models.CASCADE)
	title = models.CharField(max_length=200)
	body = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.title

	class Meta:
		ordering = ['title', 'created_at']


class Comment(MPTTModel):
	user = models.ForeignKey(User, related_name='comment', on_delete=models.CASCADE)
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
		on_delete=models.SET_NULL,
	)

	class MPTTMeta:
		order_insertion_by = ['created_at']

	def __str__(self):
		return self.body

	def save(self, *args, **kwargs):
		try:
			self.post = self.parent.post
		except AttributeError:
			pass
		super().save(*args, **kwargs)
