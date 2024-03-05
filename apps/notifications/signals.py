from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.mail.models import Email
from .handlers import notification_handler
from apps.notifications.models import Notification

receiver(post_save, sender=Email)


def send_email_notifications(sender, instance, created, **kwargs):
    """
    Sends email notifications to recipients when a new email is saved.
    """
    if created:
        notification_handler(
            actor=instance.sender,
            recipient=instance.recipient,
            verb='E',
            action_object=instance,
            key='new_email'
        )
