from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions
from rest_framework.pagination import LimitOffsetPagination
from posts.models import Group, Post

from .permissions import ReadOnly
from .serializers import CommentSerializer, GroupSerializer, PostSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_post(self):
        """Получение поста из бд."""
        post_id = self.kwargs.get('post_id')
        return get_object_or_404(Post, id=post_id)

    def perform_create(self, serializer):
        """Создание объекта комментария с правильным авторством."""
        serializer.save(
            author=self.request.user, post=self.get_post()
        )

    def get_queryset(self):
        "Получение комментариев к посту с помощью related_name."
        return self.get_post().comments.all()


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (ReadOnly,)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        """Создание объекта публикации с правильным авторством."""
        serializer.save(author=self.request.user)

    def get_queryset(self):
        """Оптимизируем запросы в бд."""
        queryset = super().get_queryset()
        return queryset.select_related('author', 'group')
