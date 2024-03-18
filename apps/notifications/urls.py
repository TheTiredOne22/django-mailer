from django.urls import path
from .views import handle_notification_click

app_name = 'notifications'

urlpatterns = [
    # Other URL patterns...
    path('notifications/<int:notification_id>/click/', handle_notification_click, name='notification_click'),
]
