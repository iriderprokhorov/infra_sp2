import django_filters.rest_framework
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, permissions, viewsets
from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination,
)
from reviews.models import Category, Comment, Genre, Review, Title

from .filters import CustomTitlesFilter
from .permissions import IsAdminOrSuper, ReviewComment
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitlesSerializer,
)

PERMISSION_CLASSES = [
    permissions.AllowAny,
]


class CreateListDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    pass


class TitlesViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Titles."""

    queryset = Title.objects.all()
    serializer_class = TitlesSerializer
    permission_classes = (IsAdminOrSuper,)
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = CustomTitlesFilter
    pagination_class = PageNumberPagination


class CategoryViewSet(CreateListDestroyViewSet):
    """Вьюсет для модели Category."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrSuper,)
    filter_backends = [
        django_filters.rest_framework.DjangoFilterBackend,
        filters.SearchFilter,
    ]
    search_fields = [
        "name",
    ]
    lookup_field = "slug"


class GenreViewSet(CreateListDestroyViewSet):
    """Вьюсет для модели Genre."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrSuper,)
    filter_backends = [
        django_filters.rest_framework.DjangoFilterBackend,
        filters.SearchFilter,
    ]
    filterset_fields = [
        "name",
    ]
    search_fields = [
        "name",
    ]
    lookup_field = "slug"


class CommentsViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Comments."""

    serializer_class = CommentSerializer
    permission_classes = (ReviewComment,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title_id = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        review_id = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        return Comment.objects.filter(review=review_id, review__title=title_id)

    def perform_create(self, serializer):
        review_id = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        return serializer.save(review=review_id, author=self.request.user)


class ReviewsViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Review."""

    serializer_class = ReviewSerializer
    permission_classes = (ReviewComment,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title_id = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        return Review.objects.filter(title=title_id)

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        serializer.save(title=title, author=self.request.user)
