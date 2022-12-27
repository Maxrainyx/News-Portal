from datetime import datetime, timedelta

from django.conf.global_settings import DEFAULT_FROM_EMAIL
from django.core.mail import send_mail

from .models import Post, Category


def get_subs(category):
    subs_emails = []
    for user in Category.objects.filter(category_name=category).values('subscribers__email'):
        subs_emails.append(user['subscribers__email'])
    return subs_emails


def new_post_add():
    new_post = Post.objects.all().order_by('-creation_time').first()
    if new_post:
        user_emails = []
        cat = ""
        for category in new_post.category.all():
            cat += f" {category}"
            user_emails.append(get_subs(category))
        email_subject = f"Новый пост в категории {cat}"
        email_message = f'{new_post.title}\n Подробнее: 127.0.0.1:8000/news/ {new_post.id}'

        send_mail(subject=email_subject,
                  message=email_message,
                  from_email=DEFAULT_FROM_EMAIL,
                  recipient_list=user_emails
                  )


def weekly_mail():
    new_posts = Post.objects.filter(creation_time__gt=(datetime.today() - timedelta(days=7)))
    user_emails = []
    cat = ""
    for category in new_posts.category.all():
        cat += f" {category}"
        user_emails.append(get_subs(category))
        email_subject = f"Новый пост в категории {cat}"
        email_message = f'{new_posts.title}\n Подробнее: 127.0.0.1:8000/news/{new_posts.id}'
        send_mail(subject=email_subject,
                  message=email_message,
                  from_email=DEFAULT_FROM_EMAIL,
                  recipient_list=user_emails
                  )
