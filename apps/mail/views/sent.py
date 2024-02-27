from django.shortcuts import render


def sent(request):
    return render(request, 'mailbox/sent.html')
