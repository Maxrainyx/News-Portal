from django.urls import path
from .views import (
   PostsList, PostDetail, PostCreate, PostUpdate, PostDelete, PostSearch, CategoriesList, CategoryView,
)
from django.views.decorators.cache import cache_page

urlpatterns = [
   path('', PostsList.as_view(), name='post_list'),
   path('<int:pk>', cache_page(5)(PostDetail.as_view()), name='post_detail'),
   path('categories/', CategoriesList.as_view(), name='categories'),
   path('categories/<int:pk>', CategoryView.as_view(), name='category_view'),
   path('create/', PostCreate.as_view(), name='post_create'),
   path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('search/', PostSearch.as_view(), name='post_search'),

]
