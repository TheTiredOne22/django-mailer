from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from apps.mail.models import Email
from apps.mail.utils import filter_emails


@login_required
def inbox(request):
    """
    View function for displaying the received emails of the logged-in user.
    """

    # Retrieve received emails for the current user, excluding archived ones

    emails = Email.objects.filter(recipient=request.user, is_archived_by_recipient=False,
                                  is_deleted_by_recipient=False).select_related(
        'sender').prefetch_related('replies').order_by(
        '-timestamp')

    # Retrieve search query from GET parameters
    search_query = request.GET.get('q', '')

    # Apply search filters if a query is present
    # if search_query:
    #     inbox_mail = filter_emails(emails, search_query)
    # else:
    #     inbox_mail = emails

    inbox_mail = filter_emails(emails, search_query)

    # Pagination
    paginator = Paginator(inbox_mail, 10)  # Show 10 emails per page
    page_number = request.GET.get('page')
    inbox_mail = paginator.get_page(page_number)

    if request.htmx:
        return render(request, 'mailbox/partials/inbox-search-results.html', {'inbox_mail': inbox_mail})
    else:
        return render(request, 'mailbox/inbox.html', {'inbox_mail': inbox_mail})
