from django.shortcuts import render


def read(request):
    return render(request, 'mailbox/read.html')
