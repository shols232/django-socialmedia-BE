from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import (
    PostCreateSerializer, PostListSerializer, PostReactSerializer, CommentCreateSerializer, 
    CommentSerializer, CommentPreviewSerializer
)
from account.serializers import UserMentionsSerializer
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Content
from rest_framework import status
from rest_framework.parsers import FileUploadParser
from rest_framework.decorators import api_view, authentication_classes, permission_classes


class Post(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    parser_class = (FileUploadParser,)

    def get(self, request, *args, **kwargs):
        query_set = Content.objects.order_by('-posted')
        serializer = PostListSerializer(query_set, many=True, context={'request':request})
        return Response(data=serializer.data, status=200)

    def post(self, request, *args, **kwargs):
        serializer = PostCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user)
            data = {'message':'post succesfully created'}
            return Response(data=serializer.data, status=200)

        return Response({'message':'Ooops!! Something went wrong...'}, status=400)


class UserFeed(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        query_set = Content.objects.filter(author=request.user)
        serializer = PostListSerializer(query_set, many=True, context={'request':request})
        return Response(data=serializer.data, status=200)

        return Response({'message':'Ooops!! Something went wrong...'}, status=400)


class PostDetail(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    parser_class = (FileUploadParser,)

    def get(self, request, *args, **kwargs):
        query_set = Content.objects.get(id=request.query_params['post_id'])
        serializer = PostListSerializer(query_set, context={'request':request})
        return Response(data=serializer.data, status=200)


@api_view(['POST', ])
@authentication_classes([TokenAuthentication, ])
@permission_classes([AllowAny, ])
def post_react(request):
    serializer = PostReactSerializer(data = request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        post_id = data['post_id']
        action = data['action']
        react = data['react']
        user = request.user
        post = Content.objects.get(id=post_id)
        exists = post.likes.filter(username=user.username).exists()

        if exists:
            if action == 'unlike':
                if react == 'like':
                    post.likes.remove(user)
                elif react == 'love':
                    post.loves.remove(user)
        else:
            if action == 'like':
                if react == 'like':
                    post.likes.add(user)
                elif react == 'love':
                    post.loves.add(user)
        return Response({'success':True}, status=200)
    return Response({'success':False}, status=400)


class Comment(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            post = Content.objects.get(id=request.data['post_id'])
            comment = serializer.save(author=request.user, post=post)
            response = {'id':comment.id, 'success':True}
            return Response(response, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        post = Content.objects.get(id=request.query_params['post_id'])
        if request.query_params['all'] == 'true':
            serializer = CommentSerializer(post.comments.all(), many=True)
        else:
            if request.query_params['specific'] == 'true':
                serializer = CommentSerializer(
                    post.comments.get(id=request.query_params['comment_id']))
            else:
                serializer = CommentPreviewSerializer(post.comments.last(), many=False)
            
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserMentions(generics.ListAPIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    
    def get(self, request, *args, **kwargs):
        if request.query_params['queryExists'] == 'true':
            username = request.query_params['username']
            users = User.objects.filter(username__contains=username).exclude(username=request.user.username)[:10]
        else:
            users = User.objects.all().exclude(username=request.user.username)[:10]
        serializer = UserMentionsSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# def echo_post(request):
#     post_id = request.POST['post_id']
#     post = Content.objects.get(id=post_id)
#     print(request.POST)
#     form = ContentForm(request.POST or None, request.FILES or None)
#     if form.is_valid():
#         obj = form.save(commit=False)
#         print(obj, obj.parent)
#         obj.parent = post
#         obj.author = request.user
#         print(obj, obj.parent)
#         obj.save()
#         return JsonResponse({"success":True})
#     return JsonResponse({"success":False})
