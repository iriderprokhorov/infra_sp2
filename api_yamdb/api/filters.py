from django_filters import CharFilter, FilterSet
from reviews.models import Title

# isort прошел два раза-ничего не поменялось


class CustomTitlesFilter(FilterSet):
    """Фильтр по полям genre, cetagory, name для модели Titles."""

    genre = CharFilter(field_name="genre__slug", lookup_expr="icontains")
    category = CharFilter(field_name="category__slug", lookup_expr="icontains")
    name = CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Title
        fields = ["year"]
