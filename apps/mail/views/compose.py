from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from apps.mail.forms import EmailComposeForm
from apps.mail.models import Email
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
            
            messages.success(request, 'Email sent successfully')
            return redirect('mail:read', slug=email.slug)
    else:
        form = EmailComposeForm()
    return render(request, 'mailbox/compose.html', {'form': form})
