from django.urls import path
from .views import account_settings, custom_logout_view

app_name = 'users'

urlpatterns = [
    path('', account_settings, name='account_settings'),
    path('accounts/logout/', custom_logout_view, name='account_logout'),
]
