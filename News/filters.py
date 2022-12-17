from django_filters import FilterSet, DateFilter
from django import forms
from .models import Post


# Создаем свой набор фильтров для модели Post.
class PostFilter(FilterSet):
    class Meta:
        filter_date = DateFilter(
            field_name='creation_type',
            widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            lookup_expr='gt',
            label='Start Date',
        )
        model = Post
        fields = {

            'title': ['contains'],
            'text': ['exact'],
            'creation_time': ['gt'],
            'type': ['exact'],
            'author': ['exact'],
        }
