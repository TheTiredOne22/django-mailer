from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Notification


# Create your views here.


def notification_list(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(recipient=request.user, read=False).distinct()
        # count = notifications.count
        return {'notifications': notifications}
    return {}
