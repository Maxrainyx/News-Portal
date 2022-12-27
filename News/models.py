from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse


class Author(models.Model):
    """ Модель, содержащая объекты всех авторов. """
    # имя Автора
    full_name = models.CharField(max_length=255)
    # связь o-t-m с моделью User (встроенная)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # рейтинг Автора
    rating = models.IntegerField(default=0)

    def update_rating(self):
        """ Метод для обновления рейтинга.
            Суммарный рейтинг каждой статьи автора умножается на 3;
            Суммарный рейтинг всех комментариев автора;
            Суммарный рейтинг всех комментариев к статьям автора. """
        # рейтинг каждой статьи автора
        post_rating = Post.objects.filter(author_id=self.id).aggregate(Sum('rating'))['rating__sum'] * 3
        # рейтинг всех комментариев автор
        us_id = self.user_id
        comment_rating = Comment.objects.filter(user_id=us_id).aggregate(Sum('rating'))['rating__sum']

        # id всех постов автора для поисков по комментариям
        author_posts_id = Post.objects.filter(author_id=self.id).values('id')

        y = []  # стартовый список для подсчета рейтинга
        for i in range(len(author_posts_id)):  # цикл поиска по количеству найденных постов в author_posts_id
            a = author_posts_id[i]['id']  # id постов этого автора
            # добавляем сумму рейтингов комментариев найденных в a -> id
            y.append(Comment.objects.filter(post_id=a).aggregate(Sum('rating'))['rating__sum'])
        author_posts_comment_rating = sum(y)  # суммируем рейтинг всех комментариев к статьям автора
        # получаем общий рейтинг автора
        result = post_rating + comment_rating + author_posts_comment_rating

        self.rating = result
        self.save()  # сохраняем результат

    def __str__(self):
        return f'{self.full_name}'


class Category(models.Model):
    """ Модель категорий новостей/статей — темы, которые они отражают (спорт, политика, образование и т. д.). """
    category_name = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User)

    def __str__(self):
        return f'{self.category_name}'

    def new_sub(self):
        return f'{self.subscribers}'


# выбор статья или новость для модели Post
article = 'A'  # запись в базе если - статья
news = 'N'  # запись в базе если - новость
TYPE = [  # лист сетов
    (article, 'Статья'),
    (news, 'Новость'),
]


class Post(models.Model):
    """ Модель содержит в себе статьи и новости, которые создают пользователи. """
    # выбор статья или новость
    type = models.CharField(max_length=255, choices=TYPE, default=article)
    # дата и время создания статьи
    creation_time = models.DateTimeField(auto_now_add=True)
    # заголовок статьи/новости
    title = models.CharField(max_length=255)
    # текст статьи/новости
    text = models.TextField()
    # рейтинг статьи/новости
    rating = models.IntegerField(default=0)

    # связь o-t-m с моделью Author
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    # связь m-t-m с моделью Category (с дополнительной моделью PostCategory)
    category = models.ManyToManyField(Category)

    def preview(self):
        """ Метод, который возвращает начало статьи(предварительный просмотр) длиной 124 символа
         и добавляет многоточие в конце."""
        return f"{self.text[:30]}..."

    def like(self):
        """ Метод для увеличения рейтинга """
        self.rating += 1
        self.save()

    def dislike(self):
        """ Метод для уменьшения рейтинга """
        self.rating -= 1
        self.save()

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def get_category(self):

        return " ".join([str(p) for p in self.category.all()])




"""    def __str__(self):
        return f'{self.author}'"""

class PostCategory(models.Model):
    """ Промежуточная модель для связи «многие ко многим» (Post, Category) """
    # связь o-t-m с моделью Post
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    # связь m-t-m с моделью Category
    category = models.ManyToManyField(Category)


class Comment(models.Model):
    """ Модель для хранения комментариев. """
    # текст комментария
    text = models.TextField()
    # дата и время создания комментария
    creation_time = models.DateTimeField(auto_now_add=True)
    # рейтинг комментария
    rating = models.IntegerField(default=0)

    # связь o-t-m с моделью Post
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    # связь o-t-m с моделью User (встроенная)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        """ Метод для увеличения рейтинга """
        self.rating += 1
        self.save()

    def dislike(self):
        """ Метод для уменьшения рейтинга """
        self.rating -= 1
        self.save()
