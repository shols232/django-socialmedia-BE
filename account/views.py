from rest_framework.generics import CreateAPIView, ListAPIView, ListCreateAPIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from .serializers import CreateUserSerializer, UserSerializer, ProfileSerializer, UserFollowingSerializer
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import Profile, UserFollowing
from rest_framework.parsers import FileUploadParser
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, authentication_classes, permission_classes


class UserRegistration(CreateAPIView):
    serializer_class = CreateUserSerializer
    permission_classes = [AllowAny, ]

    def post(self, request, *args, **kwargs):
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            account = serializer.save()
            user = serializer.data
            user_info = {
                'id':account.id,
                'token': Token.objects.get(user=account).key,
                'username':account.username, 'profile_picture':account.profile.image.url, 
                'first_name':account.first_name, 'last_name':account.last_name,
            }
            return Response(data=user_info, status=201)
        return Response({'message': 'Account could not be created'}, status=400)


class UserLogin(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'id':user.id,
                'first_name':user.first_name,
                'last_name':user.last_name,
                'profile_picture':user.profile.image.url,
                'username':user.username,
            })


class UserProfile(ListCreateAPIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    parser_class = (FileUploadParser,)

    def get(self, request, *args, **kwargs):
        profile = Profile.objects.get(user__username=request.query_params['username'])
        serializer = ProfileSerializer(profile, context={'request':request})
        return Response(serializer.data, status=200)

    def post(self, request, *args, **kwargs):
        profile = Profile.objects.get(user__username=request.query_params['username'])
        print(profile)
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid(raise_exception=True):
            obj = serializer.save()
            print(obj)
            return Response({'message':'Profile updated succesfully!'})

@api_view(['POST', ])
@authentication_classes([TokenAuthentication, ])
@permission_classes([AllowAny, ])
def follow_action(request):
    data = request.data
    following_user = request.user
    username = data.get('username')
    action = data.get('action')
    user = User.objects.get(username=username)
    follows = user.followers.filter(following_user_id=following_user).exists()

    if action == 'follow':
        if not follows:
            UserFollowing.objects.create(following_user_id=following_user,user_id=user)
            return Response({'status':'success'})
    elif action == 'unfollow':
        if follows:
            rel = UserFollowing.objects.get(following_user_id=following_user,user_id=user)
            rel.delete()
            return Response({'status':'success'})

    return Response({'status':'failed'}, safe=False)

class UserFollowings(ListAPIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        user = request.user
        followers = user.followers.all()
        serializer = UserFollowingSerializer(followers, context={'request':request}, many=True)
        return Response(serializer.data, status=200)