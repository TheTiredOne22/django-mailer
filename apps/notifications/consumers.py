from channels.generic.websocket import AsyncWebsocketConsumer
import json


class NotificationsConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        user = self.scope['user']
        if user.is_authenticated:
            await self.accept()

            await self.channel_layer.group_add(
                f'notifications_{user.id}', self.channel_name)
        else:
            await self.close()

    async def disconnect(self, close_code):
        user = self.scope['user']
        if user.is_authenticated:
            await self.channel_layer.group_discard(
                f'notifications_{user.id}', self.channel_name)

    async def send_notification(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(
            text_data=json.dumps({
                'message': message
            }))
