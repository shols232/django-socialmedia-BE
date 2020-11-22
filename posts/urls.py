from django.urls import path
from .views import *

urlpatterns = [
    path('create/', Post.as_view()),
    path('list', Post.as_view()),
    path('detail', PostDetail.as_view()),
    path('feed', UserFeed.as_view()),
    path('react/', post_react),
    path('comment/new', Comment.as_view()),
    path('comments', Comment.as_view()),
    path('mentions/users', UserMentions.as_view())
]