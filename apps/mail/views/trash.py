from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, get_list_or_404, redirect

from apps.mail.models import UserEmailAction, Email
from apps.mail.utils import filter_emails


def trash(request):
    user = request.user
    emails = Email.objects.filter(
        useremailaction__user=user,
        useremailaction__archived=True,
        useremailaction__deleted=False
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


# @login_required
# def trash(request):
#     user = request.user
#     emails = Email.objects.filter(
#         models.Q(sender=user, useremail__deleted=True) |
#         models.Q(recipient=user, useremail__deleted=True)
#     ).select_related('sender', 'recipient')
#     context = {'emails': emails}
#     return render(request, 'trash.html', context)


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
