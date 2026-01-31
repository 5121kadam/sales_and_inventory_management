from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import User
from .models import Profile

def handle_profile_creation(sender, instance, created, **kwargs):
    """
    Signal handler to create or update a Profile when usaer is saved.
    """
    if created:
        Profile.objects.create(user=instance)
        print("Profile created")
    else:
        instance.profile.save()
        print("Profile updated")