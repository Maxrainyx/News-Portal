from datetime import datetime, timedelta

from NewsPortal.settings import DEFAULT_FROM_EMAIL
from django.core.mail import send_mail

from .models import Post, Category
from celery import shared_task
import time


def get_subs(category):
    subs_emails = []
    for user in Category.objects.filter(category_name=category).values('subscribers__email'):
        subs_emails.append(user['subscribers__email'])
    return subs_emails


@shared_task
def new_post_add():
    new_post = Post.objects.all().order_by('-creation_time').first()
    if new_post:
        user_emails = []
        cat = ""
        for category in new_post.category.all():
            cat += f" {category}"
            user_emails += get_subs(category)
        email_subject = f"Новый пост в категориях: {cat}"
        email_message = f'{new_post.title}\n Подробнее: 127.0.0.1:8000/news/ {new_post.id}'

        send_mail(subject=email_subject,
                  message=email_message,
                  from_email=DEFAULT_FROM_EMAIL,
                  recipient_list=user_emails,
                  fail_silently=False,
                  )


@shared_task
def weekly_mail():
    new_posts = Post.objects.filter(creation_time__gt=(datetime.today() - timedelta(days=7)))

    post_dict = {}
    for post in new_posts:
        post_dict[str(post.id)] = post.title

    user_emails = []
    for category in new_posts.category.all():
        user_emails += get_subs(category)

    for post in post_dict:
        email_subject = f"Новое за неделю!"
        email_message = f'{post_dict[post]}\n Подробнее: https://127.0.0.1:8000/news/{post} \n'
        send_mail(subject=email_subject,
                  message=email_message,
                  from_email=DEFAULT_FROM_EMAIL,
                  recipient_list=user_emails,
                  fail_silently=False,
                  )

