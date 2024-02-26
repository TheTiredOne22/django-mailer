from django.db import models
from django.conf import settings
import uuid

# Create your models here.
from django.urls import reverse

User = settings.AUTH_USER_MODEL


class Email(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_emails')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_emails', blank=True)
    subject = models.CharField(max_length=255, blank=True)
    body = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=16, unique=True, default=uuid.uuid4, editable=False, blank=True)
    thread = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', null=True, blank=True)

    def get_absolute_url(self):
        """
        Returns the absolute URL for viewing the email.
        """
        return reverse('read', args=[str(self.slug)])

    def get_replies(self):
        """
        Retrieves replies for this email.
        """
        return self.replies.all().order_by('timestamp').select_related('sender')


class UserEmailActions(models.Model):
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
    email = models.ForeignKey(Email, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
