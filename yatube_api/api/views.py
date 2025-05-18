from rest_framework import viewsets, permissions
from rest_framework.pagination import LimitOffsetPagination

from posts.models import Post
from .serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        """Создание объекта с правильным авторством."""
        serializer.save(author=self.request.user)

    def get_queryset(self):
        """Оптимизируем запросы в бд."""
        queryset = super().get_queryset()
        return queryset.select_related('author')  # , 'group'
