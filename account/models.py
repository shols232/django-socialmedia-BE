from django.db import models
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
import sys 
from io import BytesIO 
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile

User = get_user_model()


from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.urls import reverse

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=350, default='')
    image = models.ImageField(default='default/default.png', upload_to='profile')
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

    def save(self):
        # Opening the uploaded image
        im = Image.open(self.image)

        output = BytesIO()

        # Resize/modify the image
        im = im.resize((200, 200))

        # after modifications, save it to the output
        im.save(output, format='PNG', quality=90)
        output.seek(0)

        # change the imagefield value to be the newley modifed image value
        self.image = InMemoryUploadedFile(output, 'ImageField', "%s.png" % self.image.name.split('.')[0], 'image/jpeg',
                                        sys.getsizeof(output), None)

        super(Profile, self).save()



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
