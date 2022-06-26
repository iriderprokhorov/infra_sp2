from django.db.models import Avg
from rest_framework import serializers, status
from reviews.models import Category, Comment, Genre, Review, Title


class GenreField(serializers.SlugRelatedField):
    """Пользовательский тип поля genre."""

    def to_representation(self, value):
        return GenreSerializer(value).data

    def to_internal_value(self, data):
        try:
            return self.get_queryset().get(**{self.slug_field: data})
        except (TypeError, ValueError):
            self.fail("type or value error")


class CategoryField(serializers.SlugRelatedField):
    """Пользовательский тип поля category."""

    def to_representation(self, value):
        return CategorySerializer(value).data

    def to_internal_value(self, data):
        try:
            return self.get_queryset().get(**{self.slug_field: data})
        except (TypeError, ValueError):
            self.fail("type or value error")


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Category."""

    class Meta:
        model = Category
        fields = (
            "name",
            "slug",
        )


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre."""

    class Meta:
        model = Genre
        fields = (
            "name",
            "slug",
        )


class TitlesSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title."""

    genre = GenreField(
        many=True, slug_field="slug", queryset=Genre.objects.all()
    )

    category = CategoryField(
        slug_field="slug", queryset=Category.objects.all()
    )

    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "rating",
            "description",
            "genre",
            "category",
        )

    def get_rating(self, obj):
        rating = obj.reviews.all().aggregate(Avg("score"))
        return rating["score__avg"]


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )

    class Meta:
        fields = ("id", "text", "author", "pub_date")
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Review."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )

    class Meta:
        fields = ("id", "text", "author", "score", "pub_date")
        model = Review

    def validate(self, data):
        title = self.context["request"].parser_context["kwargs"]["title_id"]
        author = self.context["request"].user
        review = Review.objects.filter(title_id=title, author=author)
        if self.context["request"].method == "POST":
            if review.exists():
                raise serializers.ValidationError(
                    detail="Только один отзыв.",
                    code=status.HTTP_400_BAD_REQUEST,
                )
        return data

    def validate_score(self, value):
        if not (1 <= value <= 10):
            raise serializers.ValidationError("From 1 to 10!")
        return value
