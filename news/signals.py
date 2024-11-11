from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import NewsArticle


@receiver(post_delete, sender=NewsArticle)
def model_deleted(sender, instance, **kwargs):
    print(instance)
