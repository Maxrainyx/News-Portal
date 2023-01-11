from django_filters import FilterSet
from .models import Post


# Создаем свой набор фильтров для модели Post.
class PostFilter(FilterSet):
    class Meta:
        model = Post
        fields = {

            'title': ['contains'],
            'text': ['exact'],
            'creation_time': ['gt'],
            'type': ['exact'],
            'author': ['exact'],
            'category': ['exact'],
        }


class CategoryFilter(FilterSet):
    class Meta:
        model = Post
        fields = {}
