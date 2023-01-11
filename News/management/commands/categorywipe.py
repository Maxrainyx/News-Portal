from django.core.management.base import BaseCommand, CommandError
from News.models import Post, Category


class Command(BaseCommand):
    help = 'Удаляет категорию взятую из аргумента.'  # показывает подсказку при вводе "python manage.py <ваша команда> --help"
    requires_migrations_checks = True  # напоминать ли о миграциях.
    # Если true — то будет напоминание о том, что не сделаны все миграции (если такие есть)

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('name', type=str)

    def handle(self, *args, **options):
        name = str(options['name'])  # переменная для получения аргумента
        # здесь можете писать любой код, который выполнится при вызове вашей команды
        self.stdout.readable()
        self.stdout.write(  # спрашиваем пользователя, действительно ли он хочет удалить все товары
            f'Do you really want to delete all posts in category {name}?\n'
        )
        answer = input('yes/no`: ')  # считываем подтверждение

        if answer == 'yes':  # в случае подтверждения действительно удаляем все товары
            posts = Post.objects.all()

            for post in posts:
                p = post.category.all()  # получаем querySet всех категорий поста, если есть. В пустом вернет None

                if p:  # проверяем есть ли категория у поста, если нет (p = None), то весь код ниже не выполнится
                    p_id = p.id  # сохраняем id поста для дальнейшего удаления

                    for category in p:  # проходим по категориям поста, т.к. их может быть несколько
                        c = category.category_name  # присвоение С значения имени категории (например, 'Общая')

                        if c == name:  # если С равна введенному аргументу значит это искомый результат!
                            Post.objects.get(id=p_id).delete()  # взять пост по id и удалить
                            # сообщение успешного удаления поста
                            print(f'Successfully deleted Post with id {p_id} in category {name}.\n')

                # сообщение об успешном удалении объектов введенной категории
                self.stdout.write(self.style.SUCCESS(f"Successfully wiped category {name}!\n"))
            return

        self.stdout.write(self.style.ERROR('Access denied\n'))  # сообщение при ошибке

