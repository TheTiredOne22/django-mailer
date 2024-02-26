from django.urls import path
from .views import inbox, compose_email

app_name = 'mail'

urlpatterns = [
    path('', inbox, name="inbox"),
    path('compose/', compose_email, name="compose")
]
