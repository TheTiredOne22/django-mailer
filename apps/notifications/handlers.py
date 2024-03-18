# from asgiref.sync import async_to_sync
# from channels.layers import get_channel_layer
# from django.contrib.auth import get_user_model
#
# from apps.notifications.models import Notification
#
#
# def notification_handler(actor, recipient, verb, **kwargs):
#     key = kwargs.pop('key', 'notification')
#     id_value = kwargs.pop('id_value', None)
#
#     if recipient == 'global':
#         users = get_user_model().objects.all().exclude(email=actor.email)
#         for user in users:
#             Notification.objects.create(
#                 actor=actor,
#                 recipient=user,
#                 verb=verb,
#                 action_object=kwargs.pop('action_object', None)
#             )
#         notification_broadcast(actor, key)
#
#     elif isinstance(recipient, get_user_model()):
#         Notification.objects.create(
#             actor=actor,
#             recipient=recipient,
#             verb=verb,
#             action_object=kwargs.pop('action_object', None)
#         )
#         notification_broadcast(actor, key, id_value=id_value, recipient=recipient.email)
#
#     else:
#         pass
#
#
# def notification_broadcast(actor, key, **kwargs):
#     channel_layer = get_channel_layer()
#     id_value = kwargs.pop('id_value', None)
#     recipient = kwargs.pop('recipient', None)
#     payload = {
#         'type': 'receive',
#         'key': key,
#         'actor_name': f'{actor.first_name} {actor.last_name}',
#         'id_value': id_value,
#         'recipient': recipient,
#
#     }
#     async_to_sync(channel_layer.group_send)('notifications', payload)
