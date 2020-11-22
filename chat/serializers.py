from rest_framework import serializers
from .models import Chat, Messages, Contact
from account.serializers import UserSerializer
from django.contrib.auth.models import User

class MessagesSerializer(serializers.ModelSerializer):
    sender_username = serializers.SerializerMethodField()

    class Meta:
        model = Messages
        fields = ['sender_username', 'content', 'timestamp']

    def get_sender_username(self, message):
        return message.contact.user.username
    
class ChatSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    last_message_sent = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = ['id', 'user', 'last_message_sent']
        depth = 2

    def get_last_message_sent(self, chat):
        print(chat.messages.last())
        message = chat.messages.last()
        serializer = MessagesSerializer(message)
        return serializer.data

    def get_user(self, chat):
        try:
            user = self.context['request'].user
        except KeyError:
            user = self.context['user']
        if chat.user_one.user == user:
            user_2 = chat.user_two.user
        else:
            user_2 = chat.user_one.user
        print(user, chat.user_one, chat.user_two)
        serializer = UserSerializer(user_2)
        return serializer.data

class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = '__all__'

class ChatCreateSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(max_length=20, write_only=True)

    class Meta:
        model = Chat
        fields = ['user_id']

    def create(self, validated_data):
        req_user = self.context['request'].user
        user_id = validated_data['user_id']
        user = User.objects.get(id=user_id)
        contact, created = Contact.objects.get_or_create(user=user)
        req_contact, created = Contact.objects.get_or_create(user=req_user)

        try:
            chat = Chat.objects.get(user_one=req_contact, user_two=contact)
        except:
            try:
                chat = Chat.objects.get(user_one=contact, user_two=req_contact)
            except:
                chat = Chat.objects.create(user_one=req_contact, user_two=contact)

        return ChatSerializer(chat, context={'user':req_user}).data


