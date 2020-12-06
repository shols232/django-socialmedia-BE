from rest_framework import serializers
from .models import Content, Comment, Reply
from account.serializers import ProfileSerializer, UserSerializer
from rest_framework.serializers import ValidationError



class PostCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Content
        fields = ['content', 'image_content']
        extra_kwargs = {'image_content': {'required': False}}

    def create(self, validated_data):
        return super().create(validated_data)


class PostListSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField(read_only=True)
    first_three_pics = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    loves = serializers.SerializerMethodField()
    likes_post = serializers.SerializerMethodField()
    loves_post = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    username = serializers.CharField(read_only=True, source='author.username')
    author_pic = serializers.CharField(read_only=True, source='author.profile.image.url')
    country = serializers.CharField(read_only=True, source='author.profile.country')
    state = serializers.CharField(read_only=True, source='author.profile.state')

    class Meta:
        model = Content
        exclude = ['author',]

    def get_likes(self, obj):
        return obj.likes.count()

    def get_loves(self, obj):
        return obj.loves.count()

    def get_likes_post(self, obj):
        user = self.context['request'].user
        return obj.likes.filter(username=user.username).exists()

    def get_loves_post(self, obj):
        user = self.context['request'].user
        return obj.loves.filter(username=user.username).exists()

    def get_owner(self, obj):
        return obj.author.first_name + ' ' + obj.author.last_name

    def get_comments_count(self, obj):
        return obj.comments.count()

    def get_first_three_pics(self, obj):
        final_comments = []
        comments = Comment.objects.filter(post__id=obj.id)[:3]
        for comment in comments:
            final_comments.append(comment.author.profile.image.url)
        return final_comments


class PostReactSerializer(serializers.Serializer):
    post_id = serializers.CharField(max_length=15)
    action = serializers.CharField(max_length=15)
    react = serializers.CharField(max_length=15)


class ReplySerializer(serializers.ModelSerializer):
    author = UserSerializer(source='reply.author')

    class Meta:
        model = Reply
        fields = '__all__'

class CommentPreviewSerializer(serializers.ModelSerializer):
    replies = serializers.CharField(source='replies.count')
    author = UserSerializer()

    class Meta:
        model = Comment
        exclude = ['post']


class CommentSerializer(serializers.ModelSerializer):
    replies = ReplySerializer(many=True)
    author = UserSerializer()

    class Meta:
        model = Comment
        exclude = ['post']


class CommentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['content']



    




