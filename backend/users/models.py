from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver


User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    subscriptions = models.ManyToManyField(
        'self',
        symmetrical=False,
        through='Subscription',
        through_fields=('follower', 'author')
    )

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class Subscription(models.Model):
    follower = models.ForeignKey(
        'Profile',
        on_delete=models.CASCADE,
        related_name='subscribed_on'
    )

    author = models.ForeignKey(
        'Profile',
        on_delete=models.CASCADE,
        related_name='followers'
    )

    date_of_subscription = models.DateTimeField(auto_now_add=True)
