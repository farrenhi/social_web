from django.db.models.signals import post_save
# will be send at the end of save method

from django.contrib.auth.models import User
# User model

from django.dispatch import receiver
# register the signal. use receiver decorator

from .models import Profile, Relationship
# profile model

# a communication between User and Profile
@receiver(post_save, sender=User)
def post_save_created_profile(sender, instance, created, **kwargs):
    print('sender', sender)
    print('instance', instance)
    # a new user is created, then a new profile is created to this user.
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=Relationship)
def post_save_add_to_friends(sender, instance, created, **kwargs):
    sender_ = instance.sender
    receiver_ = instance.receiver
    if instance.status == 'accepted':
        sender_.friends.add(receiver_.user)
        receiver_.friends.add(sender_.user)
        sender_.save()
        receiver_.save()
        
        
        
    