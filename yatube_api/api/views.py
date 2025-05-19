from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, mixins, filters
from rest_framework.pagination import LimitOffsetPagination
from posts.models import Group, Post, Follow

from .permissions import IsOwnerOrReadOnly
from .serializers import (
    CommentSerializer, GroupSerializer, PostSerializer, FollowSerializer
)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        IsOwnerOrReadOnly, permissions.IsAuthenticatedOrReadOnly
    )

    def get_post(self):
        """Получение поста из бд."""
        post_id = self.kwargs.get('post_id')
        return get_object_or_404(Post, id=post_id)

    def get_queryset(self):
        "Получение комментариев к посту с помощью related_name."
        return self.get_post().comments.all()

    def perform_create(self, serializer):
        """Создание объекта комментария с правильным авторством."""
        serializer.save(
            author=self.request.user, post=self.get_post()
        )


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.AllowAny,)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (
        IsOwnerOrReadOnly, permissions.IsAuthenticatedOrReadOnly
    )
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        """Оптимизируем запросы в бд."""
        queryset = super().get_queryset()
        return queryset.select_related('author', 'group')

    def perform_create(self, serializer):
        """Создание объекта публикации с правильным авторством."""
        serializer.save(author=self.request.user)


class FollowViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    """ViewSet подписок с кастомным наследованием
    для обработки только двух эндпоинтов.
    """
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)

    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Создание объекта подписки с правильным авторством."""
        serializer.save(user=self.request.user)
