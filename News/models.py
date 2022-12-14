from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    """ Модель, содержащая объекты всех авторов. """
    # имя Автора
    full_name = models.CharField(max_length=255)
    # связь o-t-m с моделью User (встроенная)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # рейтинг Автора
    rating = models.IntegerField(default=0)

    def update_rating(self, aa, ac, caa):
        """ Метод для обновления рейтинга.
            Суммарный рейтинг каждой статьи автора(-aa-) умножается на 3;
            Суммарный рейтинг всех комментариев автора(-ac-);
            Суммарный рейтинг всех комментариев к статьям автора(-caa-). """
        self.aa = aa
        self.ac = ac
        self.caa = caa
        self.rating += (aa*3+ac+caa)  # расчет по заданной формуле
        self.save()


class Category(models.Model):
    """ Модель категорий новостей/статей — темы, которые они отражают (спорт, политика, образование и т. д.). """
    category_name = models.CharField(max_length=255, unique=True)


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
        return f"{self.text[:124]}..."

    def like(self):
        """ Метод для увеличения рейтинга """
        self.rating += 1
        self.save()

    def dislike(self):
        """ Метод для уменьшения рейтинга """
        self.rating -= 1
        self.save()


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
