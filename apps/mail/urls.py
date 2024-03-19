from django.urls import path
from .views import inbox, compose_email, archive, read_email, sent, starred, trash, toggle_starred_email, \
    bulk_archive_email, bulk_trash_email, toggle_archive_email, toggle_trash_email

app_name = 'mail'

urlpatterns = [
    path('', inbox, name="inbox"),
    path('compose/', compose_email, name="compose"),
    path('archive/', archive, name="archive"),
    path('read/<slug:slug>/', read_email, name='read'),
    path('sent/', sent, name='sent'),
    path('starred/', starred, name='starred'),
    path('trash/', trash, name='trash'),

    path('star-email/<slug:slug>/', toggle_starred_email, name='star_email'),
    path('archive-email/<slug:slug>/', toggle_archive_email, name='archive_email'),
    path('trash-email/<slug:slug>/', toggle_trash_email, name='trash_email'),
    path('bulk-archive/', bulk_archive_email, name='bulk_archive'),

    path('bulk-trash/', bulk_trash_email, name='bulk_trash')
]
