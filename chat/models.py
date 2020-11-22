from django.db import models
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save

User = get_user_model()

class Contact(models.Model):
    user = models.ForeignKey(User, related_name="contacts", on_delete=models.CASCADE)
    friends = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.user.username

class Messages(models.Model):
    contact = models.ForeignKey(Contact, related_name='contact_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.contact.user.username

    def last_10_messages(self):
        
        return Messages.objects.order_by('-timestamp')[:10]


class Chat(models.Model):
    user_one = models.ForeignKey(Contact, on_delete=models.PROTECT, related_name="chats")
    user_two = models.ForeignKey(Contact, related_name="chats_2", on_delete=models.PROTECT)
    messages = models.ManyToManyField(Messages, blank=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pk)

    def last_message(self):
        try:
            return self.messages.last().content
        except AttributeError:
            return ''

@receiver(post_save, sender=User)
def create_contact(sender, instance, created, **kwargs):
    if created:
        Contact.objects.create(user=instance)

'''to be converted for group chats later.... by ferrum-san ofcourse'''
# class Chat(models.Model):
#     partcipants = models.ManyToManyField(Contact, related_name="chats")
#     messages = models.ManyToManyField(Messages, blank=True)


#     def last_10_messages(self):
#             return Messages.objects.order_by('-timestamp')[:10]

#     def __str__(self):
#         return str(self.pk)