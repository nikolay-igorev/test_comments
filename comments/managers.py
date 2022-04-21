from django.db import models
from django.db.models import Max, Min


class CommentManager(models.Manager):
    # Менеджер для дерева комментариев
    def comments_tree(self, comment=None, post=None, limit=None):
        # Для списка ответов к комментарию
        if comment:
            queryset = [comment]
            min_nesting = comment.nesting + 1
            max_nesting = super().get_queryset().aggregate(Max('nesting'))['nesting__max']

        # Для списка комментариев к посту
        elif post:
            queryset = super().get_queryset().filter(post=post).order_by('post_id')
            if queryset:
                min_nesting = queryset.aggregate(Min('nesting'))['nesting__min']
                max_nesting = queryset.aggregate(Max('nesting'))['nesting__max']
                queryset = list(queryset.filter(nesting=min_nesting))
                min_nesting += 1

        # Для полного списка комментариев
        else:
            queryset = list(super().get_queryset().filter(nesting=1).order_by('post_id'))
            min_nesting = 2
            max_nesting = super().get_queryset().aggregate(Max('nesting'))['nesting__max']

        if queryset:
            # Полное дерево комментариев или до 3 уровня вложенности
            if limit:
                full_queryset = super().get_queryset().filter(nesting__in=[n for n in range(min_nesting-1, min_nesting+2)])
            else:
                full_queryset = super().get_queryset()

            # Создание сортированного списка комментариев
            for nesting in range(min_nesting, max_nesting + 1):
                for comment in full_queryset.filter(nesting=nesting):
                    parent_pk = comment.parent_id
                    try:
                        parent_index = queryset.index(full_queryset.get(pk=parent_pk))
                        queryset.insert(parent_index + 1, comment)
                    except ValueError:
                        pass

        return queryset

