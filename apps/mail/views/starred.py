from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template.response import TemplateResponse
from django.views.decorators.http import require_POST
from apps.mail.models import Email, UserEmailAction
from apps.mail.utils import filter_emails


def starred(request):
    """
    Filter starred emails for the current user, whether they were the sender or recipient.
    Order the emails by timestamp, so the most recent ones appear first.
    """
    emails = Email.objects.filter(
        Q(sender=request.user, is_starred_by_sender=True) |
        Q(recipient=request.user, is_starred_by_recipient=True)
    ).order_by('-timestamp')

    # Retrieve search query from GET parameters
    search_query = request.GET.get('q')

    if search_query:
        starred_emails = filter_emails(emails, search_query)
    else:
        starred_emails = emails

    paginator = Paginator(starred_emails, 10)  # Show 10 emails per page
    page_number = request.GET.get('page')
    starred_emails = paginator.get_page(page_number)

    if request.htmx:
        return render(request, 'mailbox/partials/search/starred-search-results.html',
                      {'starred_emails': starred_emails})
    else:
        # Render the archive page with the retrieved emails
        return render(request, 'mailbox/starred.html', {'starred_emails': starred_emails})


@require_POST
def toggle_starred_email(request, slug):
    """
    View to toggle the starred status of a specific email.
    """
    # Retrieve the email to toggle starred status
    email = get_object_or_404(Email, slug=slug)
    user_action, created = UserEmailAction.objects.get_or_create(
        user=request.user,
        email=email
    )
    user_action.toggle_star()
    context = {
        'email': email,
        'user_action': user_action
    }
    return TemplateResponse(request, 'mailbox/partials/star-icon.html', context)
