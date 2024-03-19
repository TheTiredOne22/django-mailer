from django.template.loader import render_to_string
from django.http import HttpResponse

from apps.notifications.models import Notification


def update_notification_count(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(recipient=request.user, read=False)
        count = notifications.count()
        context = {'notification_count': count}
        html = render_to_string('notification/notification-count-partial.html', context, request=request)
        return HttpResponse(html)
    return HttpResponse('')
