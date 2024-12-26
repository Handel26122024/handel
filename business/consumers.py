import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model

User = get_user_model()

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]

        if not self.user.is_authenticated:
            await self.close()

        self.group_name = f'user_{self.user.id}'

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)

        if data.get('action') == 'mark_as_viewed':
            await self.mark_notifications_as_viewed()

    async def notify(self, event):
        await self.send(text_data=json.dumps(event["content"]))

    @sync_to_async
    def mark_notifications_as_viewed(self):
        self.user.notifications.filter(is_viewed=False).update(is_viewed=True)

        for notification in self.user.notifications.filter(is_viewed=True):
            async_to_sync(self.channel_layer.group_send)(
                f'user_{notification.order.customer.id}', {
                    'type': 'notify',
                    'content': {
                        'message': f'Your order #{notification.order.id} has been viewed by the shop admin.',
                        'order_id': notification.order.id,
                        'is_viewed': True,
                    }
                }
            )
