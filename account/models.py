from django.db import models
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model

User = get_user_model()


from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.urls import reverse

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=350, default='')
    image = models.ImageField(default='default/default.png')
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=400, blank=True, null=True, default='')
    country = models.CharField(max_length=200,blank=True, null=True, default='Afghanistan')
    state = models.CharField(max_length=250, blank=True, null=True, default='')
    phone_number = models.CharField(max_length=15, blank=True, null=True, default='')
    work_exp = models.CharField(max_length=900, blank=True, null=True, default='')
    extra_info = models.CharField(max_length=900, blank=True, null=True, default='')

    # def get_absolute_url(self):
    #     return reverse('profile', args=[self.user.id])

    def __str__(self):
        return self.user.username



class UserFollowing(models.Model):
    user_id = models.ForeignKey(User, related_name="followers", on_delete=models.CASCADE)
    following_user_id = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        unique_together = ("user_id", "following_user_id")
        ordering = ["-created"]

    def __str__(self):
        return f"{self.following_user_id.username} follows {self.user_id.username}"


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        
@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


# class Hashtag(models.Model):
#     hash_text = models.CharField(max_length=55)
#     posts = models.ManyToManyField(HashesPostsIds)
#     count = models.BigIntegerField()


# class HashesPostsIds(models.Model):
#     post_id = models.CharField(max_length=20)
