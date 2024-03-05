import uuid

from django.db import models
from django.urls import reverse
from django.conf import settings

User = settings.AUTH_USER_MODEL


# Create your models here.


class MessageQueryset(models.query.QuerySet):
    # def get_inbox_messages(self, recipient):
    #     """
    #     Returns all the emails where the user is the recipient
    #     """
    #     return self.filter(recipient=recipient, useremailaction__archived=False,
    #                        useremailaction__deleted=False).distinct()

    def get_sent_messages(self, sender):
        """
        Returns all emails where the user is the sender
        """
        return self.filter(sender=sender, useremailaction__archived=False,
                           useremailaction__deleted=False).distinct()


class Email(models.Model):
    """
    Represents an email message.
    """
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user')
    subject = models.CharField(max_length=255)
    body = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=36, unique=True, default=uuid.uuid4, editable=False, blank=True)
    is_read = models.BooleanField(default=False)
    parent_email = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE,
                                     related_name='reply_parent')
    objects = MessageQueryset.as_manager()

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        """
        Returns a string representation of the email.
        """
        return f"{self.subject} - {self.sender.email}"

    def get_absolute_url(self):
        """
        Returns the absolute URL for viewing the email.
        """
        return reverse('read', args=[str(self.slug)])

    def mark_as_read(self):
        """
        Marks the email as read.
        """
        if not self.is_read:
            self.is_read = True
            self.save()

    def get_replies(self):
        """
        Retrieve replies for this email.
        """
        return self.replies.all()


class UserEmailAction(models.Model):
    """
    Tracks user-specific actions on emails (archived, starred, deleted).
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.ForeignKey(Email, on_delete=models.CASCADE)
    archived = models.BooleanField(default=False)
    starred = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    def toggle_archive(self):
        """
        Toggle the archive status of the email for the user
        """
        self.archived = not self.archived
        self.save()

    def toggle_star(self):
        """
        Toggle the starred status of the email for the user
        """
        self.starred = not self.starred
        self.save()

    def toggle_delete(self):
        """
        Toggle the deleted status of the email for the user
        """
        self.deleted = not self.deleted
        self.save()


class Reply(models.Model):
    """
    Represents a reply to an email.
    """
    email = models.ForeignKey(Email, on_delete=models.CASCADE, related_name='replies')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_replies')
    # recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_replies')
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
