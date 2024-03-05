import uuid

from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from slugify import slugify
from django.utils.timesince import timesince

# Create your models here.
User = settings.AUTH_USER_MODEL


class NotificationQueryset(models.query.QuerySet):

    def unread(self):
        """Returns unread notifications in the current queryset"""
        return self.filter(read=False)

    def unread_notification_count(self):
        """Returns the count of all unread notifications in the current queryset"""
        return self.filter(read=False).count()


class Notification(models.Model):
    NEW_EMAIL = 'E'
    REPLY = 'R'
    NOTIFICATION_TYPES = (
        (NEW_EMAIL, "new email"),
        (REPLY, "replied")
    )
    actor = models.ForeignKey(User,
                              related_name='notify_actor',
                              on_delete=models.CASCADE)
    recipient = models.ForeignKey(User,
                                  blank=False,
                                  related_name='notifications',
                                  on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    uuid_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=210, null=True, blank=True)
    verb = models.CharField(max_length=1, choices=NOTIFICATION_TYPES)
    action_object_content_type = models.ForeignKey(
        ContentType,
        blank=True,
        null=True,
        related_name='notify_action_object',
        on_delete=models.CASCADE
    )
    action_object_object_id = models.CharField(max_length=50, blank=True, null=True)
    action_object = GenericForeignKey(
        'action_object_content_type', 'action_object_object_id'
    )
    objects = NotificationQueryset.as_manager()

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ('-timestamp',)

    def __str__(self):
        if self.action_object:
            return f'{self.actor} {self.get_verb_display()} {self.action_object} {self.time_since()} ago '
        return f'{self.actor} {self.get_verb_display()} {self.action_object} {self.time_since} ago'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(
                f"{self.recipient} {self.uuid_id} {self.verb}",
                lowercase=True,
                max_length=200,
            )

        super().save(*args, **kwargs)

    def time_since(self, now=None):
        return timesince(self.timestamp, now)

    def mark_as_read(self):
        if self.read:
            self.read = True
            self.save()

    def mark_as_unread(self):
        if not self.read:
            self.read = False
            self.save()
