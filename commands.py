"""
1. Создать двух пользователей (с помощью метода User.objects.create_user('username')):"""
from News.models import *

user1 = User.objects.create_user('Username1')
user2 = User.objects.create_user('Username2')
"""
2. Создать два объекта модели Author, связанные с пользователями:"""
author1 = Author.objects.create(full_name='Max', user_id=1)
author2 = Author.objects.create(full_name='Denis', user_id=2)
"""
3. Добавить 4 категории в модель Category:"""
cat1 = Category.objects.create(category_name='Общая')
cat2 = Category.objects.create(category_name='Спорт')
cat3 = Category.objects.create(category_name='Погода')
cat4 = Category.objects.create(category_name='Путешествия')
"""
4. Добавить 2 статьи и 1 новость:"""
post1 = Post(title='Спортивный заголовок 1', text='Спортивный текст 1', author_id=1)
post1.save()
post2 = Post(title='Спортивный заголовок 2', text='Спортивный текст 2', author_id=2)
post2.save()
post3 = Post(type = news, title='Новость 1', text='Новостной текст 2', author_id=1)
post3.save()
"""
5. Присвоить им категории (как минимум в одной статье/новости должно быть не меньше 2 категорий):"""
post1.category.add(1,2,3)
post2.category.add(2)
post3.category.add(3)
"""
6. Создать как минимум 4 комментария к разным объектам модели Post
(в каждом объекте должен быть как минимум один комментарий)."""
com1 = Comment.objects.create(text='Текст комментария 1', post_id=1, user_id=2)
com2 = Comment.objects.create(text='Текст комментария 2', post_id=3, user_id=1)
com3 = Comment.objects.create(text='Текст комментария 3', post_id=2, user_id=2)
com4 = Comment.objects.create(text='Текст комментария 4', post_id=1, user_id=1)
"""
7. Применяя функции like() и dislike() к статьям/новостям и комментариям, скорректировать рейтинги этих объектов."""
post1.like()
post1.like()
post2.dislike()
post3.like()
post2.dislike()
post1.like()
com3.like()
com2.dislike()
com4.like()
"""
8. Обновить рейтинги пользователей."""
author1.update_rating(4,0,0)
author2.update_rating(-3,0,0)
"""
9. Вывести username и рейтинг лучшего пользователя (применяя сортировку и возвращая поля первого объекта)."""
best_user = Author.objects.order_by('-rating').values('full_name','rating').first()
print(f"{bu['full_name']}, {bu['rating']}")
"""
10. Вывести дату добавления, +username автора, рейтинг, +заголовок и +превью лучшей статьи,
основываясь на лайках/дислайках к этой"""
best_post = Post.objects.order_by('-rating').values('id', 'creation_time', 'rating', 'title').first()
best_post_id = best_post['id']
best_post_preview = Post.objects.get(id=best_post_id).preview()
best_post_author_id = Post.objects.order_by('-rating').values().first()['author_id']  # id из Post для поиска в User
best_post_username = User.objects.filter(id=best_post_author_id).values('username')[0]['username']
best_post_title = best_post['title']
best_post_date = best_post['creation_time']
best_post_rating = best_post['rating']

print(f"Дата:{best_post_date}, пользователь: {best_post_username}, рейтинг: {best_post_rating}, \nзаголовок: {best_post_title}, \nпревью: {best_post_preview}")
"""
11. Вывести все комментарии (дата, пользователь, рейтинг, текст) к этой статье."""
best_post_comments = Comment.objects.filter(post_id=best_post_id).values('creation_time', 'user_id', 'rating', 'text')

for i in best_post_comments:
    print(f"Дата: {i['creation_time']}")
    print(f"Пользователь: {User.objects.filter(id=i['user_id']).values('username')[0]['username']}")
    print(f"Рейтинг: {i['rating']}")
    print(f"Текст:{i['text']}")
    print("---"*6)
