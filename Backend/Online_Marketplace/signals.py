from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import User as AuthUser
from .models import UserProfile, Category

@receiver(post_save, sender=AuthUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_migrate)
def seed_data(sender, **kwargs):
    if sender.name == "Online_Marketplace":

        categories = ["men", "women", "kids", "clothes", "sports", "toys"]

        for name in categories:
            Category.objects.get_or_create(categoryName=name)        