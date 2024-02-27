from django.shortcuts import render


def trash(request):
    return render(request, 'mailbox/trash.html')
