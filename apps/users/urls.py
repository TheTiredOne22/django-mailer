from django.urls import path
from .views import account_settings

app_name = 'users'

urlpatterns = [
    path('', account_settings, name='account_settings')
]
