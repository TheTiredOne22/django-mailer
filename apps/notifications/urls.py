from django.urls import path
from .views import update_notification_count

app_name = 'notifications'

urlpatterns = [
    # Other URL patterns...
    path('update_notification_count/', update_notification_count, name='update_notification_count'),

]
