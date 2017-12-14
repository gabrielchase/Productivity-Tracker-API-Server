from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.contrib.auth import get_user_model
User = get_user_model()


class Category(models.Model):

    name = models.CharField(max_length=255, primary_key=True)
    
    def __str__(self):
        return self.name


class Activity(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    end_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    productive = models.BooleanField()
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name="activities", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


def pre_save_activity(sender, instance, *args,  **kwargs):
    # if kwargs.get('created', False):
    #     UserProfile.objects.get_or_create(user=kwargs.get('instance'))
    print('BOYBOYBOY')

pre_save.connect(pre_save_activity, sender=Activity)