from django.shortcuts import render, redirect, get_object_or_404

from apps.mail.forms import EmailReplyForm
from apps.mail.models import Email, Reply
from apps.notifications.models import Notification


def read_email(request, slug):
    """
    Display details of a specific email and handle email replies.
    """
    email = get_object_or_404(Email, slug=slug)

    # Mark email as read if the authenticated user is the recipient
    if request.user == email.recipient:
        email.mark_as_read()

    #     notification = Notification.objects.filter(user=request.user, related_email=email).first()
    #     if notification:
    #         notification.mark_as_read()
    #
    #     # Mark reply notifications as read when a user opens a reply
    # unread_reply_notifications = Notification.objects.filter(
    #     user=request.user,
    #     notification_type=Notification.NotificationType.REPLY,
    #     related_email=email,
    #     is_read=False
    # )
    #
    # for notification in unread_reply_notifications:
    #     notification.mark_as_read()

    # Retrieve replies
    replies = email.get_replies()

    # Handle the reply form
    form = handle_reply_form(request, email)

    context = {'email': email, 'replies': replies, 'form': form}
    return render(request, 'mailbox/read.html', context)


def handle_reply_form(request, email):
    """
    Handle the email reply form.
    """
    if request.method == 'POST':
        form = EmailReplyForm(request.POST)
        if form.is_valid():
            new_reply = form.save(commit=False)
            new_reply.sender = request.user
            new_reply.email = email
            new_reply.save()
            return redirect('mail:read', slug=email.slug)
    else:
        form = EmailReplyForm()
    return form
