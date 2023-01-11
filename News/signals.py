from .tasks import new_post_add, get_subs
from django.dispatch import receiver
from .models import Post
from django.db.models.signals import m2m_changed
from django.core.mail import send_mail
from NewsPortal.settings import DEFAULT_FROM_EMAIL


@receiver(m2m_changed, sender=Post)
def notify_subs(sender, instance, **kwargs):
    new_post = Post.objects.all().order_by('-creation_time').first()
    if new_post:
        user_emails = []
        cat = ""
        for category in new_post.category.all():
            cat += f" {category.category_name}"
            user_emails += get_subs(category.category_name)
        email_subject = f"Новый пост в категориях: {cat}"
        email_message = f'{new_post.title}\n Подробнее: http://127.0.0.1:8000/news/{new_post.id}'

        send_mail(subject=email_subject,
                  message=email_message,
                  from_email=DEFAULT_FROM_EMAIL,
                  recipient_list=user_emails,
                  fail_silently=False,
                  )
