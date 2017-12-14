from rest_framework import serializers

from django.contrib.auth import get_user_model
User = get_user_model()

from activities.models import (Activity, Category)
from activities.serializers import UserSerializer


class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ('name')


class ActivitySerializer(serializers.ModelSerializer):

    user = UserSerializer()
    category = CategorySerializer()

    class Meta: 
        model = Activity
        fields = (id, name, description, start_time, end_time, productive, user, category)