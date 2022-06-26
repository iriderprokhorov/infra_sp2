from django.contrib import admin

from .models import Comment, Review, Title, Category


class TitleAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "year", "category")
    search_fields = ("name",)
    list_filter = ("year",)
    empty_value_display = "-пусто-"


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("text", "author", "pub_date", "score")


admin.site.register(Title, TitleAdmin)
admin.site.register(Comment)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Category)
