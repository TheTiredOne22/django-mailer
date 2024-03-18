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

        # Mark related notifications as read
        notifications = Notification.objects.filter(action_object_object_id=email.id)
        notifications.update(read=True)

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
