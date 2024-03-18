from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.mail.models import Email, Reply
from apps.notifications.models import Notification


@receiver(post_save, sender=Email)
def send_email_notifications(sender, instance, created, **kwargs):
    """
    Sends email notifications to recipients when a new email is sent.
    """
    if created:
        channel_layer = get_channel_layer()
        notification = Notification.objects.create(
            actor=instance.sender,
            recipient=instance.recipient,
            verb=Notification.NEW_EMAIL,
            action_object=instance,

        )
        async_to_sync(channel_layer.group_send)(
            f'notifications_{instance.recipient.id}', {
                'type': 'send_notification',
                'notification': {
                    'actor': str(notification.actor),
                    'verb': notification.get_verb_display(),
                    'action_object': str(notification.action_object),
                    'time_since': notification.time_since()
                }
            }
        )


@receiver(post_save, sender=Reply)
def send_reply_notification(sender, instance, created, **kwargs):
    if created:
        email = instance.email
        if email.sender != instance.sender:
            channel_layer = get_channel_layer()
            notification = Notification.objects.create(
                actor=instance.sender,
                recipient=email.sender,
                verb=Notification.REPLY,
                action_object=instance,
            )

            async_to_sync(channel_layer.group_send)(
                f'notifications_{email.sender.id}',
                {
                    'type': 'send_notification',
                    'notification': {
                        'actor': str(notification.actor),
                        'verb': notification.get_verb_display(),
                        'action_object': str(notification.action_object),
                        'time_since': notification.time_since()
                    }
                }
            )
