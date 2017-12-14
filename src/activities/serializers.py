from rest_framework import serializers
from rest_framework.renderers import JSONRenderer

from django.contrib.auth import get_user_model
User = get_user_model()


from activities.models import (Activity, Category)
from users.serializers import (UserSerializer, DetailSerializer)
from users.models import Details

import json


class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ('name',)


class ActivitySerializer(serializers.ModelSerializer):

    user_details = serializers.SerializerMethodField()
    category = CategorySerializer()

    class Meta: 
        model = Activity
        fields = (
            'id', 'name', 'description', 'start_time', 'end_time', 'productive', 
            'category', 'user_details'
        )

    def get_user_details(self, obj):
        user_details = {
            'id': obj.user.id,
            'first_name': obj.user.first_name,
            'last_name': obj.user.last_name,
            'email': obj.user.email,
            'username': obj.user.username,
            'date_joined': obj.user.date_joined.isoformat(),
            'country': obj.user.details.country,
            'goal': obj.user.details.goal, 
            'mobile_number': obj.user.details.goal
        }

        return json.loads(json.dumps(user_details))
