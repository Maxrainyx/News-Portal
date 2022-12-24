
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import PermissionRequiredMixin
from .models import Post
from .filters import PostFilter
from .forms import PostForm
from django.urls import reverse_lazy
from django.shortcuts import render, redirect


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
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    # Используем другой шаблон — post.html
    template_name = 'post.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'post'


    def post(self, request, *args, **kwargs):
        p_k = self.request.path.split("/")[-1]
        category = Post.objects.filter(id=pk).values('category__category_name')
        for i in category:
            m = str(i['category__category_name'])
            x = Category.objects.get(category_name=(request.POST.get(m, 'Общая')))
            x.subscribers.add(request.user.id)

        """
        html_content = render_to_string(
            'sub_done.html'
        )

        # в конструкторе уже знакомые нам параметры, да? Называются правда немного по-другому, но суть та же.
        msg = EmailMultiAlternatives(
             subject=f'{category.category_name}',
             body=self.category.message,  # это то же, что и message
             from_email='maxrainyx@yandex.ru',
             to=['maxrainy@gmail.com'],  # это то же, что и recipients_list
         )
         msg.attach_alternative(html_content, "text/html")  # добавляем html

         msg.send()  # отсылаем"""

        return redirect(f"/news/{p_k}")


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

