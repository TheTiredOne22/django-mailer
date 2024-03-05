from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from apps.mail.forms import EmailComposeForm
from apps.mail.models import Email
from apps.notifications.handlers import notification_handler
from apps.notifications.models import Notification


@login_required
def compose_email(request):
    if request.method == 'POST':
        form = EmailComposeForm(request.POST)
        if form.is_valid():
            sender = request.user
            recipient = form.cleaned_data['recipient']
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']

            # Create the email instance
            email = Email.objects.create(sender=sender, subject=subject, body=body, recipient=recipient)
            # Send notification to the recipient
            notification_handler(actor=sender, recipient=recipient, verb=Notification.NEW_EMAIL, action_object=email)
            return redirect('mail:read', slug=email.slug)
    else:
        form = EmailComposeForm()
    return render(request, 'mailbox/compose.html', {'form': form})
