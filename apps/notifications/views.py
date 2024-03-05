from django.shortcuts import render

# Create your views here.
from django.template.response import TemplateResponse


def unread_notification_list(request):
    notification_list = request.user.notifications.unread()
    notification_count = notification_list.count()
    context = {
        'notification_list': notification_list,
        'notification_count': notification_count,
    }
    return TemplateResponse(request, 'notifications/notification_list.html', context)
