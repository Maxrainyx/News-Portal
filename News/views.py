from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView,
)
from django.contrib.auth.mixins import PermissionRequiredMixin
from .models import Post, Category, Comment, User
from .filters import PostFilter
from .forms import PostForm
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.core.cache import cache


class PostsList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-creation_time'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'news.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'news'
    paginate_by = 20


class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    # Используем другой шаблон — post.html
    template_name = 'post.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'post'

    def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта, как ни странно
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
        return obj

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        users = list()
        comments = list(Comment.objects.filter(post_id=self.kwargs["pk"]).values('id', 'text', 'user_id', 'creation_time'))
        for comment in comments:
            user_name = User.objects.filter(id=comment['user_id']).values('username')[0]['username']
            users.append(user_name)

        context['comment_text'] = {
            'text': comments,
            'user': users,
        }
        return context


class CategoriesList(ListView):
    model = Category
    template_name = 'categories.html'
    context_object_name = 'categories'
    paginate_by = 20

    def get(self, request, *args, **kwargs):
        category = Category.objects.all()
        return render(request, 'categories.html', {"category": category})


class CategoryView(DetailView):
    model = Category
    template_name = 'category.html'
    context_object_name = 'category'
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        context['category_post'] = list(
            Post.objects.filter(category=self.kwargs["pk"]).values('title', 'text', 'rating')
        )
        return context

    def post(self, request, pk, *args, **kwargs):
        category = Category.objects.get(id=self.kwargs["pk"])
        category.subscribers.add(request.user.id)
        return redirect('categories')


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('News.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        path = self.request.path
        if 'news' in path:
            post.type = 'N'
        else:
            post.type = 'A'
        post.author_id = self.request.user.author.id
        return super().form_valid(form)


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('News.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


# Представление удаляющее товар.
class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


class PostSearch(ListView):
    model = Post
    context_object_name = 'news'
    template_name = 'post_search.html'
    ordering = '-creation_time'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


