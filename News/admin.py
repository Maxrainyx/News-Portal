from django.contrib import admin
from .models import Post, Category, Comment


def nullify_rating(modeladmin, request, queryset):
    # все аргументы уже должны быть вам знакомы, самые нужные из них это request — объект хранящий информацию
    # о запросе и queryset — грубо говоря набор объектов, которых мы выделили галочками.
    queryset.update(rating=0)


nullify_rating.short_description = 'Обнулить рейтинг'


# Register your models here
class PostAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ('type', 'rating', 'creation_time', 'title', 'author')
    list_filter = ('type', 'rating', 'author', 'creation_time', 'category__category_name')
    search_fields = ('author__full_name', 'category__category_name')
    actions = [nullify_rating]


class CommentAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ('creation_time', 'rating', 'post', 'user')
    list_filter = ('rating', 'user', 'creation_time', )
    actions = [nullify_rating]


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Comment, CommentAdmin)
