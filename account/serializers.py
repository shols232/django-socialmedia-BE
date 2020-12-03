from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile, UserFollowing, UserSettings
from posts.models import Content

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.first_name = validated_data['first_name']
        user.last_name = validated_data['last_name']
        user.save()
        return user


class ProfileSerializer(serializers.ModelSerializer):
    following = serializers.SerializerMethodField(read_only=True)
    followers = serializers.SerializerMethodField(read_only=True)
    owner = serializers.SerializerMethodField(read_only=True)
    image = serializers.ImageField(required=False)
    follows = serializers.SerializerMethodField(read_only=True)
    post_counts = serializers.SerializerMethodField(read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Profile
        exclude = ['user']

    def get_following(self, obj):
        following = obj.user.following.count()
        return following

    def get_followers(self, obj):
        followers = obj.user.followers.count()
        return followers

    def get_post_counts(self, obj):
        user = self.context['request'].user
        print(Content.objects.filter(author=user).count())
        return Content.objects.filter(author=user).count()

    def get_follows(self, obj):
        user = self.context['request'].user
        follows = obj.user.followers.filter(following_user_id=user).exists()
        return follows

    def get_owner(self, obj):
        user = self.context['request'].user
        if user == obj.user:
            return True
        else:
            return False

class UserSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    bio = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 
        'bio', 'image_url']

    def get_image_url(self, user):
        return user.profile.image.url

    def get_bio(self, user):
        print(user.profile.bio, user)
        return user.profile.bio


class UserMentionsSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'image_url']

    def get_image_url(self, user):
        return user.profile.image.url


class UserFollowingSerializer(serializers.ModelSerializer):
    user = UserSerializer(source='user_id')

    class Meta:
        model = UserFollowing
        fields = ['user']

class UserSettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserSettings
        exclude = ['user']

