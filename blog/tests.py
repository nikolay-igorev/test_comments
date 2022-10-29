import random

from django.contrib.auth import get_user_model
from django.db.models import Q
from django.urls import reverse
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.test import override_settings

from .models import Post, Comment

client = APIClient()
User = get_user_model()


@override_settings(MPTT_ALLOW_TESTING_GENERATORS=True)
class PostTest(APITestCase):
	def setUp(self) -> None:

		for _ in range(random.randint(2, 10)):
			baker.make(User)

		self.users = User.objects.filter(is_superuser=False)
		self.user1 = self.users.order_by('?').first()
		self.user2 = self.users.filter(~Q(id=self.user1.id)).order_by('?').first()

		for _ in range(random.randint(2, 10)):
			baker.make(Post, user=self.users.order_by('?').first())

		self.post_user1 = baker.make(Post, user=self.user1)

		self.posts = Post.objects.all()
		self.post = self.posts.order_by('?').first()
		self.posts_count = self.posts.count()

		self.data = {'title': 'title', 'body': 'body'}

	def test_post_list(self):
		url = reverse('post-list')
		response = self.client.get(url)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(self.posts.count(), len(response.data))
		self.assertEqual(url, '/api/v1/posts/')

	def test_post_create(self):
		self.client.force_authenticate(self.user1)

		url = reverse('post-list')
		response = self.client.post(url, data=self.data)

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(self.posts_count + 1, Post.objects.count())

	def test_post_create_wrong_user(self):
		self.client.force_authenticate(self.user1)
		posts_count = self.posts.count()

		url = reverse('post-list')
		response = self.client.post(url, data=self.data.update({'user': self.user2}))
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(self.posts_count, Post.objects.count())

	def test_post_create_anon(self):
		posts_count = self.posts.count()
		url = reverse('post-list')
		response = self.client.post(url, data=self.data)

		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
		self.assertEqual(posts_count, self.posts.count())

	def test_post_retrieve(self):
		url = reverse('post-detail', args=(self.post.id,))
		response = self.client.get(url)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(url, f'/api/v1/posts/{self.post.id}/')
		self.assertEqual(response.data['id'], self.post.id)

	def test_post_update(self):
		self.client.force_authenticate(self.user1)

		url = reverse('post-detail', args=(self.post_user1.id,))
		response = self.client.patch(url, data=self.data)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['body'], self.data['body'], Post.objects.get(id=self.post_user1.id).body)

	def test_post_update_wrong_user(self):
		self.client.force_authenticate(self.user2)

		url = reverse('post-detail', args=(self.post_user1.id,))
		response = self.client.patch(url, data=self.data)

		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
		self.assertNotEquals(self.post.body, self.data['body'])

	def test_post_update_anon(self):
		url = reverse('post-detail', args=(self.post.id,))
		response = self.client.patch(url, data=self.data)

		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
		self.assertNotEquals(self.post.body, self.data['body'])

	def test_post_delete(self):
		self.client.force_authenticate(self.user1)

		url = reverse('post-detail', args=(self.post_user1.id,))
		response = self.client.delete(url)

		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
		self.assertEqual(self.posts_count - 1, Post.objects.count())

	def test_post_delete_wrong_user(self):
		self.client.force_authenticate(self.user2)

		url = reverse('post-detail', args=(self.post_user1.id,))
		response = self.client.delete(url)

		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
		self.assertEqual(self.posts_count, Post.objects.count())

	def test_post_delete_anon(self):
		url = reverse('post-detail', args=(self.post_user1.id,))
		response = self.client.delete(url)

		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
		self.assertEqual(self.posts_count, Post.objects.count())


class CommentTest(APITestCase):
	@override_settings(MPTT_ALLOW_TESTING_GENERATORS=True)
	def setUp(self) -> None:

		for _ in range(random.randint(2, 10)):
			baker.make(User)

		self.users = User.objects.filter(is_superuser=False)
		self.user1 = self.users.order_by('?').first()
		self.user2 = self.users.filter(~Q(id=self.user1.id)).order_by('?').first()

		for _ in range(random.randint(2, 10)):
			baker.make(Post, user=self.users.order_by('?').first())

		self.posts = Post.objects.all()
		self.post = self.posts.order_by('?').first()

		for _ in range(random.randint(2, 10)):
			baker.make(
				Comment,
				user=self.users.order_by('?').first(),
				post=self.posts.order_by('?').first()
			)
		for _ in range(random.randint(2, 10)):
			baker.make(
				Comment,
				user=self.users.order_by('?').first(),
				parent=Comment.objects.order_by('?').first()
			)

		self.post_user1 = baker.make(
			Post,
			user=self.user1
		)

		self.comment_user1 = baker.make(
			Comment,
			user=self.user1,
			post=Post.objects.filter((~Q(user=self.user2))).order_by('?').first()
		)

		self.comment_post_user1 = baker.make(
			Comment,
			user=self.user2,
			post=self.post_user1
		)

		self.comments = Comment.objects.all()
		self.comment = self.comments.order_by('?').first()

		self.comments_count = self.comments.count()

		self.data = {'body': 'body'}

	def test_comments_list(self):
		url = reverse('comment-list')
		response = self.client.get(url)

		comments_order_response = [comment['id'] for comment in response.data]
		comments_order_queryset = [comment.id for comment in Comment.objects.order_by('tree_id', 'lft')]

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(url, '/api/v1/comments/')
		self.assertEqual(comments_order_response, comments_order_queryset)

	def test_comments_post_create(self):
		self.client.force_authenticate(self.user1)
		url = reverse('comment-post-create', args=(self.post.id,))
		response = self.client.post(url, data=self.data)

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(url, f'/api/v1/posts/{self.post.id}/comments/')
		self.assertEqual(self.comments_count + 1, Comment.objects.count())
		self.assertEqual(response.data['user'], self.user1.id)
		self.assertEqual(response.data['post'], self.post.id)
		self.assertEqual(response.data['parent'], None)
		self.assertEqual(response.data['level'], 0)

	def test_comments_post_create_anon(self):
		url = reverse('comment-post-create', args=(self.post.id,))
		response = self.client.post(url, data=self.data)

		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
		self.assertEqual(self.comments_count, Comment.objects.count())

	def test_comments_child_create(self):
		self.client.force_authenticate(self.user1)

		url = reverse('comment-child-create', args=(self.comment.id,))
		response = self.client.post(url, data=self.data)

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(url, f'/api/v1/comments/{self.comment.id}/comments/')
		self.assertEqual(self.comments_count + 1, Comment.objects.count())
		self.assertEqual(response.data['user'], self.user1.id)
		self.assertEqual(response.data['post'], self.comment.post.id)
		self.assertEqual(response.data['parent'], self.comment.id)
		self.assertEqual(response.data['level'], self.comment.get_level() + 1)

	def test_comments_child_create_anon(self):
		url = reverse('comment-child-create', args=(self.comment.id,))
		response = self.client.post(url, data=self.data)

		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
		self.assertEqual(self.comments_count, Comment.objects.count())

	def test_comments_retrieve(self):
		url = reverse('comment-detail', args=(self.comment.id,))
		response = self.client.get(url)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(url, f'/api/v1/comments/{self.comment.id}/')
		self.assertEqual(response.data['id'], self.comment.id)

	def test_comments_update(self):
		self.client.force_authenticate(self.user1)

		url = reverse('comment-detail', args=(self.comment_user1.id,))
		response = self.client.patch(url, data=self.data)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['body'], self.data['body'], Comment.objects.get(id=self.comment_user1.id))

	def test_comments_update_wrong_user(self):
		self.client.force_authenticate(self.user2)

		url = reverse('comment-detail', args=(self.comment_user1.id,))
		response = self.client.patch(url, data=self.data)

		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
		self.assertNotEquals(self.comment_user1.body, self.data['body'])

	def test_comments_update_anon(self):
		url = reverse('comment-detail', args=(self.comment_user1.id,))
		response = self.client.patch(url, data=self.data)

		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
		self.assertNotEquals(self.comment_user1.body, self.data['body'])

	def test_comments_delete(self):
		self.client.force_authenticate(self.user1)

		url = reverse('comment-detail', args=(self.comment_user1.id,))
		response = self.client.delete(url)

		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
		self.assertEqual(self.comments_count - 1, Comment.objects.count())

	def test_comments_delete_post_owner(self):
		self.client.force_authenticate(self.user1)

		url = reverse('comment-detail', args=(self.comment_post_user1.id,))
		response = self.client.delete(url)

		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
		self.assertEqual(self.comments_count - 1, Comment.objects.count())

	def test_comments_delete_wrong_user(self):
		self.client.force_authenticate(self.user2)

		url = reverse('comment-detail', args=(self.comment_user1.id,))
		response = self.client.delete(url)

		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
		self.assertEqual(self.comments_count, Comment.objects.count())

	def test_comments_delete_anon(self):
		url = reverse('comment-detail', args=(self.comment.id,))
		response = self.client.delete(url)

		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
		self.assertEqual(self.comments_count, Comment.objects.count())
