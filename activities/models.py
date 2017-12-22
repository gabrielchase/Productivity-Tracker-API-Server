from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.contrib.auth import get_user_model
User = get_user_model()


class Category(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name


class Activity(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=True)
    start_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    end_time = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    productive = models.BooleanField()
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='activities', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
