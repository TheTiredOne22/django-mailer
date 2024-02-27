from django.shortcuts import render


def archive(request):
    return render(request, 'mailbox/archive.html')
