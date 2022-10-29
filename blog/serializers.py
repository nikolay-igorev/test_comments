from rest_framework import serializers

from .models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
	class Meta:
		model = Post
		fields = ('id', 'user', 'title', 'body', 'created_at',)
		read_only_fields = ('id', 'user',)


class CommentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Comment
		fields = ('id', 'user', 'body', 'created_at', 'post', 'parent', 'lft', 'rght', 'tree_id', 'level',)
		read_only_fields = ('user', 'post', 'parent', 'lft', 'rght', 'tree_id', 'level',)
