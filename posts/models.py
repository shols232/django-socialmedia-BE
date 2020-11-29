from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import sys 
from io import BytesIO 
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
# from account.models import Profile

# Create your models here.


class Content(models.Model):
    parent = models.ForeignKey('self', related_name='echoes', null=True, blank=True, on_delete=models.SET_NULL)
    content = models.TextField(blank=True,null=True)
    author = models.ForeignKey(User, related_name="content", on_delete=models.CASCADE)
    posted = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, related_name='my_likes')
    loves = models.ManyToManyField(User, related_name="my_loves")
    image_content = models.ImageField(upload_to='content/', blank=True, null=True)


    @property
    def is_echo(self):
        return self.parent != None

    def __str__(self):
        return self.content[:10]

    def save(self, *args, **kwargs):
        # Opening the uploaded image
        im = Image.open(self.image_content)

        output = BytesIO()

        # Resize/modify the image
        im = im.resize((300, 300))

        # after modifications, save it to the output
        im.save(output, format='PNG', quality=90)
        output.seek(0)

        # change the imagefield value to be the newley modifed image value
        self.image_content = InMemoryUploadedFile(output, 'ImageField', "%s.png" % self.image_content.name.split('.')[0], 'image/png',
                                        sys.getsizeof(output), None)

        super(Content, self).save(*args, **kwargs)

    
# Comment threading model

# comment reply
class Reply(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    content = models.TextField(blank=True,null=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.author

# comment
class Comment(models.Model):
    post = models.ForeignKey(Content,on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    replies = models.ManyToManyField(Reply)
    created = models.DateTimeField(auto_now_add=True)
    content = models.TextField(blank=True,null=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.author

