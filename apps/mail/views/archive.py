from django.core.paginator import Paginator
from django.shortcuts import render

from apps.mail.models import Email
from apps.mail.utils import filter_emails


def archive(request):
    user = request.user
    emails = Email.objects.filter(
        useremailaction__user=user,
        useremailaction__archived=True,
        useremailaction__deleted=False
    ).distinct()

    # Retrieve search query from GET parameters
    search_query = request.GET.get('q', '')
    archived_mail = filter_emails(emails, search_query)

    # Pagination
    paginator = Paginator(archived_mail, 10)  # Show 10 emails per page
    page_number = request.GET.get('page')
    archived_mail = paginator.get_page(page_number)

    if request.htmx:
        return render(request, 'mailbox/partials/active-search/archive-search-results.html',
                      {'archived_mail': archived_mail})
    else:
        return render(request, 'mailbox/archive.html', {'archived_mail': archived_mail})
