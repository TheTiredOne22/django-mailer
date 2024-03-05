from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Email, UserEmailAction


@receiver(post_save, sender=Email)
def create_user_email(sender, instance, created, **kwargs):
    """
    Automatically create a UserEmail instance for each new Email instance.
    """
    if created:
        # Create UserEmail instance for the sender
        UserEmailAction.objects.create(user=instance.sender, email=instance)

        # Create UserEmail instance for the recipient
        UserEmailAction.objects.create(user=instance.recipient, email=instance)
