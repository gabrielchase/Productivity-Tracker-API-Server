from rest_framework import serializers
from rest_framework.renderers import JSONRenderer

from django.contrib.auth import get_user_model
User = get_user_model()


from activities.models import (Activity, Category)
from users.serializers import (UserSerializer, DetailSerializer)
from users.models import Details


class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ('name',)


class ActivitySerializer(serializers.ModelSerializer):

    user = UserSerializer()
    category = CategorySerializer()

    class Meta: 
        model = Activity
        fields = (
            'id', 'name', 'description', 'start_time', 'end_time', 'productive', 
            'user', 'category'
        )
