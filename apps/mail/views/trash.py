from django.shortcuts import render


def trash(request):
    return render(request, 'mailbox/trash.html')

# @login_required
# def trash(request):
#     user = request.user
#     emails = Email.objects.filter(
#         models.Q(sender=user, useremail__deleted=True) |
#         models.Q(recipient=user, useremail__deleted=True)
#     ).select_related('sender', 'recipient')
#     context = {'emails': emails}
#     return render(request, 'trash.html', context)
