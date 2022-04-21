from django.db.models import Max, Min
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse, resolve
from django.views.generic import ListView, CreateView

from comments.models import Comment, list_to_queryset
from posts.models import Post


# Полный список комментариев
class CommentsListView(ListView):
    model = Comment
    template_name = 'comments/comments_list.html'
    context_object_name = 'comments'

    def get_queryset(self):
        return Comment.objects.comments_tree()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"All Comments"

        queryset = list_to_queryset(self.get_queryset())
        min_nesting = queryset.aggregate(Min('nesting'))['nesting__min']

        context['oldest_posts'] = queryset\
            .filter(nesting=min_nesting)\
            .order_by('post_id')\
            .distinct('post_id')

        return context


# Список комментариев к посту
class CommentsPostListView(ListView):
    model = Comment
    template_name = 'comments/comments_list.html'
    context_object_name = 'comments'

    def get_queryset(self):
        # Список комментариев к посту до 3 уровня вложенности
        if resolve(self.request.path_info).url_name == 'comments_post_list':
            return Comment.objects.comments_tree(
                post=get_object_or_404(
                    Post, pk=self.kwargs['pk']
                ),
                limit=3
            )
        # Полный список комментариев к посту
        elif resolve(self.request.path_info).url_name == 'comments_post_all_list':
            return Comment.objects.comments_tree(
                post=get_object_or_404(
                    Post, pk=self.kwargs['pk']
                )
            )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = get_object_or_404(Post, pk=self.kwargs['pk'])
        context['title'] = f"Comments to post: \"{context['post']}\""
        context['heading'] = f"Comments to post: \"{context['post']}\""
        context['post_url'] = 'post_detail'

        if resolve(self.request.path_info).url_name == 'comments_post_list':
            context['pk'] = self.kwargs['pk']
            context['full_list_url'] = 'comments_post_all_list'

        return context


# Список ответов к комментарию
class CommentsRepliesListView(ListView):
    model = Comment
    template_name = 'comments/comments_list.html'
    context_object_name = 'comments'

    # Список ответов к комментарию до 3 уровня вложенности
    def get_queryset(self):
        if resolve(self.request.path_info).url_name == 'comment_replies_list':
            return Comment.objects.comments_tree(
                comment=get_object_or_404(
                    Comment,
                    pk=self.kwargs['pk'],
                ),
                limit=3
            )

        # Полный список ответов к комментарию
        elif resolve(self.request.path_info).url_name == 'comment_replies_all_list':
            return Comment.objects.comments_tree(
                comment=get_object_or_404(
                    Comment,
                    pk=self.kwargs['pk'],
                ),
            )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = get_object_or_404(Comment, pk=self.kwargs['pk'])
        context['title'] = f"Replies to comment: \"{context['post']}\""
        context['heading'] = f"Replies to comment: \"{context['post']}\""
        context['post_url'] = 'comment_replies_list'
        if resolve(self.request.path_info).url_name == 'comment_replies_list':
            context['pk'] = self.kwargs['pk']
            context['full_list_url'] = 'comment_replies_all_list'

        return context


# Создание комментария
class CommentCreateView(CreateView):
    model = Comment
    fields = ['body']
    template_name = 'comments/comment_form.html'

    def form_valid(self, form):
        # Если комментарий принадлежит авторизованному пользователю
        if self.request.user.is_authenticated:
            form.instance.author = self.request.user
        # Пост, к котому оставляется комментарий
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['pk'])
        # Уровень вложенности для оригинального комментария равен 1
        form.instance.nesting = 1

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = get_object_or_404(Post, pk=self.kwargs['pk'])
        context['title'] = f"Comment to post: \"{context['post']}\""
        context['heading'] = f"Comment to post: \"{context['post']}\""
        context['post_url'] = 'post_detail'

        return context

    def get_success_url(self):
        return reverse('comments_post_list', kwargs={'pk': self.kwargs['pk']})


# Создание ответа к комментарию
class CommentReplyCreateView(CreateView):
    model = Comment
    fields = ['body']
    template_name = 'comments/comment_form.html'

    def form_valid(self, form):
        # Если комментарий принадлежит авторизованному пользователю
        if self.request.user.is_authenticated:
            form.instance.author = self.request.user
        # Комментарий-родитель
        form.instance.parent = get_object_or_404(Comment, pk=self.kwargs['pk'])
        # Оригинальный пост
        form.instance.post = form.instance.parent.post
        # Уровень вложенности
        form.instance.nesting = form.instance.parent.nesting + 1

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = get_object_or_404(Comment, pk=self.kwargs['pk'])
        context['title'] = f"Reply to comment: \"{context['post']}\""
        context['heading'] = f"Reply to comment: \"{context['post']}\""
        context['post_url'] = 'comment_replies_list'

        return context

    def get_success_url(self):
        return reverse('comment_replies_list', kwargs={'pk': self.kwargs['pk']})
