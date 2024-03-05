from django.urls import path
from .views import inbox, compose_email, archive, read_email, sent, starred, trash, toggle_starred_email

app_name = 'mail'

urlpatterns = [
    path('', inbox, name="inbox"),
    path('compose/', compose_email, name="compose"),
    path('archive/', archive, name="archive"),
    path('read/<slug:slug>/', read_email, name='read'),
    path('sent/', sent, name='sent'),
    path('starred/', starred, name='starred'),
    path('trash/', trash, name='trash'),

    path('star-email/<slug:slug>/', toggle_starred_email, name='star_email')
]
