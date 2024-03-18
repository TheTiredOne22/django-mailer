from django.shortcuts import redirect, get_object_or_404
from .models import Notification


# Create your views here.
def handle_notification_click(request, notification_id):
    """
    Handle the click event on a notification to redirect users to the related email or reply.
    """
    notification = get_object_or_404(Notification, id=notification_id)

    # Mark the notification as read
    notification.read = True
    notification.save()

    # Redirect the user to the related URL
    return redirect(notification.url)
