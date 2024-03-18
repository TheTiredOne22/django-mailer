from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.template.response import TemplateResponse
from django.views.decorators.http import require_POST

from apps.mail.models import Email, UserEmailAction
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
        return render(request, 'mailbox/partials/active-search/archived-search-results.html',
                      {'archived_mail': archived_mail})
    else:
        return render(request, 'mailbox/archive.html', {'archived_mail': archived_mail})


def toggle_archive_email(request, slug):
    """
    View to toggle the starred status of a specific email.
    """
    email = get_object_or_404(Email, slug=slug)
    user_email_action, created = UserEmailAction.objects.get_or_create(
        user=request.user,
        email=email,
    )
    user_email_action.toggle_archive()
    messages.success(request, f'Email archived successfully')
    return redirect('mail:archive')


def bulk_archive_email(request):
    if request.method == 'POST':
        email_ids = request.POST.getlist('email_ids')
        emails = get_list_or_404(Email, id__in=email_ids)
        for email in emails:
            user_email_action, created = UserEmailAction.objects.get_or_create(
                user=request.user,
                email=email
            )
            user_email_action.toggle_archive()
        messages.success(request, f'{len(emails)} emails archived successfully')

    return redirect('mail:archive')
