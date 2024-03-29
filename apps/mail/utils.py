from django.db.models import Q


def filter_emails(emails, search_query):
    if search_query:
        return emails.filter(Q(subject__icontains=search_query) |
                             Q(sender__first_name__icontains=search_query) |
                             Q(sender__last_name__icontains=search_query)
                             )
    else:
        return emails
