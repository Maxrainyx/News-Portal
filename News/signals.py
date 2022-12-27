from .tasks import new_post_add as posted
from django.dispatch import receiver
from .models import PostCategory
from django.db.models.signals import m2m_changed


@receiver(m2m_changed, sender=PostCategory)
def notify_subs(sender, instance, **kwargs):
    posted()
