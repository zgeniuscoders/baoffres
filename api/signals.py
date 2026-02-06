from django.db.models.signals import post_save, post_delete
from django.core.cache import cache
from django.dispatch import receiver

from api.models import Category


@receiver([post_save, post_delete], sender=Category)
def invalidate_categories_cache(sender, instance, **kwargs):
    cache.delete_many("*categories*")
    cache.delete_many("*category*")


@receiver([post_save, post_delete], sender=Category)
def invalidate_location_cache(sender, instance, **kwargs):
    cache.delete_many("*location_list*")
    cache.delete_many("*location_detail*")
