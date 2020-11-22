from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Chat, Contact, Messages
from django.contrib.auth.models import User
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import ChatSerializer, MessagesSerializer, UserSerializer, ChatCreateSerializer
from rest_framework.response import Response
from rest_framework import status

class UserChats(ListCreateAPIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        serializer = ChatCreateSerializer(data=request.data, context={'request':request})
        if serializer.is_valid(raise_exception=True):
            data = serializer.save()
            return Response(data, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        contact = Contact.objects.filter(user=request.user).first()
        chats = contact.chats_2.all()
        chats_2 = contact.chats.all()
        total_chats = chats | chats_2
        total_chats = total_chats.order_by('-updated')
        serializer = ChatSerializer(total_chats, many=True, context={'request':request})
        print(serializer.data, total_chats)
        return Response(serializer.data, status=200)


class ChatMessages(ListAPIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]


    def list(self, request, *args, **kwargs):
        try:
            chat = Chat.objects.get(id=request.query_params['chat_id'])
        except (Chat.DoesNotExist, ValueError):
            return Response({'error':'CHAT_DOES_NOT_EXIST'}, status=status.HTTP_404_NOT_FOUND)
        qs = chat.messages.order_by('timestamp')
        serializer = MessagesSerializer(qs, many=True)
        return Response(serializer.data, status=200)


# class to return a list of users to be added as a chat option
class ChatUsers(ListAPIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def list(self, request, *args, **kwargs):
        sugg = request.query_params['suggestion']
        if len(sugg) > 0:
            qs = User.objects.filter(username__contains=sugg).exclude(username=request.user.username)
        else:
            qs = User.objects.all().exclude(username=request.user.username)
        serializer = UserSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


def get_last_100_messages(chat_id, request=None):
    try:
        chat = Chat.objects.get(id=chat_id)
    except (Chat.DoesNotExist, ValueError):
        return {'failed':True, 'message':'Chat Does Not Exist'}
    return {'failed':False, 'messages':chat.messages.order_by('-timestamp')[:100]}