from django.core.paginator import Paginator
from django.shortcuts import render

from apps.mail.models import Email, UserEmailAction
from apps.mail.utils import filter_emails


def sent(request):
    user = request.user
    emails = Email.objects.filter(
        sender=user,
        useremailaction__user=user,
        useremailaction__archived=False,
        useremailaction__deleted=False
    ).distinct()

    # Retrieve search query from GET parameters
    search_query = request.GET.get('q', '')
    sent_mail = filter_emails(emails, search_query)

    # Get starred emails for the current user
    starred_emails = UserEmailAction.objects.filter(user=user, starred=True).values_list('email__slug', flat=True)

    # Pagination
    paginator = Paginator(sent_mail, 10)  # Show 10 emails per page
    page_number = request.GET.get('page')
    sent_mail = paginator.get_page(page_number)

    if request.htmx:
        return render(request, 'mailbox/partials/active-search/sent-search-results.html', {'sent_mail': sent_mail})
    else:
        return render(request, 'mailbox/sent.html', {'sent_mail': sent_mail, 'starred_emails': starred_emails})
