from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import F
from django.shortcuts import render, get_list_or_404, redirect, get_object_or_404

from apps.mail.models import UserEmailAction, Email
from apps.mail.utils import filter_emails


def trash(request):
    user = request.user
    emails = Email.objects.filter(
        useremailaction__user=user,
        useremailaction__archived=False,
        useremailaction__deleted=True
    ).distinct()

    # Retrieve search query from GET parameters
    search_query = request.GET.get('q', '')
    trash_mail = filter_emails(emails, search_query)

    # Pagination
    paginator = Paginator(trash_mail, 10)  # Show 10 emails per page
    page_number = request.GET.get('page')
    trash_mail = paginator.get_page(page_number)

    if request.htmx:
        return render(request, 'mailbox/partials/active-search/trash-search-results.html',
                      {'trash_mail': trash_mail})
    else:
        return render(request, 'mailbox/trash.html', {'trash_mail': trash_mail})


def bulk_trash_email(request):
    if request.method == 'POST':
        email_ids = request.POST.getlist('email_ids')
        emails = get_list_or_404(Email, id__in=email_ids)
        for email in emails:
            user_email_action, created = UserEmailAction.objects.get_or_create(
                user=request.user,
                email=email
            )
            user_email_action.toggle_delete()
        messages.success(request, f'{len(emails)} emails deleted successfully')

    return redirect('mail:trash')


def toggle_trash_email(request, slug):
    """
    View to toggle the deletion status of a specific email.
    """
    email = get_object_or_404(Email, slug=slug)
    user_email_action, created = UserEmailAction.objects.get_or_create(
        user=request.user,
        email=email,
    )
    UserEmailAction.objects.filter(pk=user_email_action.pk).update(starred=~F('deleted'))

    # Retrieve the updated user_action instance
    user_email_action.refresh_from_db()
    messages.error(request, f'Email deleted successfully')
    return redirect('mail:trash')
