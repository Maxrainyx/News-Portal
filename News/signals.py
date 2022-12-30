from .tasks import new_post_add as posted
from django.dispatch import receiver
from .models import PostCategory, Post, Category
from django.db.models.signals import m2m_changed
from datetime import datetime, timedelta
from django.core.mail import send_mail
from celery import shared_task


@receiver(m2m_changed, sender=PostCategory)
def notify_subs(sender, instance, **kwargs):
    posted()
