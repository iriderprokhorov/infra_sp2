import datetime

from django.core.exceptions import ValidationError
from django.db import models
from users.models import User


class Category(models.Model):
    """Модель категории произведения."""

    name = models.CharField(
        verbose_name="Название категории",
        unique=True,
        max_length=200,
    )

    slug = models.SlugField(
        verbose_name="Слаг категории",
        unique=True,
        max_length=50,
    )

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"
        ordering = ("id",)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанров произведений."""

    name = models.CharField(verbose_name="Жанр", max_length=200)

    slug = models.SlugField(
        verbose_name="Слаг жанра",
        unique=True,
    )

    class Meta:
        verbose_name = "жанр"
        verbose_name_plural = "жанры"
        ordering = ("id",)

    def __str__(self):
        return self.name


def validate_year(value):
    # первая книга была издана в 868 г.Google
    if 868 < value < datetime.date.today().year:
        return value
    else:
        raise ValidationError(
            "Год не может быть в будущем, либо далёком прошлом"
        )


class Title(models.Model):
    """Модель произведения."""

    name = models.CharField(
        verbose_name="Название произведения", max_length=200
    )

    year = models.PositiveSmallIntegerField(
        verbose_name="Год создания произведения",
        blank=True,
        validators=[validate_year],
    )

    description = models.CharField(
        verbose_name="Описание произведения",
        max_length=200,
        blank=True,
    )

    genre = models.ManyToManyField(
        Genre,
        verbose_name="Жанр произведения",
        related_name="genre",
        blank=True,
    )
    category = models.ForeignKey(
        Category,
        verbose_name="Описание категории",
        related_name="category",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "произведение"
        verbose_name_plural = "произведения"
        ordering = ("id",)

    def __str__(self):
        return self.name


class Review(models.Model):
    """Модель отзывов."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    text = models.TextField()

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    score = models.IntegerField()
    pub_date = models.DateTimeField(
        "Дата добавления", auto_now_add=True, db_index=True
    )

    class Meta:
        verbose_name = "отзыв"
        verbose_name_plural = "отзывы"
        constraints = [
            models.UniqueConstraint(
                fields=("author", "title"), name="unique_review"
            )
        ]


class Comment(models.Model):
    """Модель комментариев."""

    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )
    pub_date = models.DateTimeField(
        "Дата добавления", auto_now_add=True, db_index=True
    )

    class Meta:
        verbose_name = "коментарий"
        verbose_name_plural = "комментариев"

    def __str__(self):
        return self.text
