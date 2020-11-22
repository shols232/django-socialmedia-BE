# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Messages, Contact, Chat
from .views import get_last_100_messages
import datetime
from django.utils.html import format_html
from .serializers import ChatSerializer, MessagesSerializer

class ChatConsumer(WebsocketConsumer):

    def fetch_messages(self, data):
        print(data)
        messages = get_last_100_messages(data['id'])
        if messages['failed']:
                self.send_message({'command':'messages', 'status':'Chat with that id does not exist'})
        else:
            serializer = ChatSerializer(messages['messages'], many=True)
            messages = serializer.data
            messages.reverse()
            content = {
                'command':'messages',
                'messages':messages
            }
            self.send_message(content)


    def new_message(self, data):
        user = self.scope['user']
        contact, created = Contact.objects.get_or_create(user=user)
        message = Messages.objects.create(contact=contact, content=data['message'])
        chat, created = Chat.objects.get_or_create(id=data["chat_id"])
        chat.messages.add(message)
        chat.updated = datetime.datetime.now()
        chat.save()
        chat_id = chat.id
        serializer = MessagesSerializer(message, context={'user':self.scope['user']})
        message = serializer.data

        content = {
            'command':'new_message',
            'chat_id':chat_id,
            'message':message
        }
        self.send_message_to_channel(content)
        

    commands = {
        'fetch_messages':fetch_messages,
        'new_message':new_message
    }


    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data_json = json.loads(text_data)
        self.commands[data_json['command']](self, data_json)

        
    def send_message_to_channel(self, message):    
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps(message))