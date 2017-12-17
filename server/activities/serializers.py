from rest_framework import serializers
from rest_framework.renderers import JSONRenderer

from django.contrib.auth import get_user_model
User = get_user_model()

from activities.models import (Activity, Category)
from activities.utils import handle_activity_category

from users.serializers import (UserSerializer, DetailSerializer)
from users.models import Details

import json


class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ('id', 'name')


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

    def create(self, data):
        category = handle_activity_category(data.pop('category', {}).get('name'))
        
        new_activity = Activity.objects.create(
            name=data.get('name'),
            description=data.get('description'),
            start_time=data.get('start_time'),
            end_time=data.get('end_time'),
            productive=data.get('productive'),
            user=self.context['request'].user,
            category=category
        )

        return new_activity
        
    def update(self, activity_instance, data):
        category = handle_activity_category(data.pop('category', {}).get('name'))

        activity_instance.name = data.get('name')
        activity_instance.description = data.get('description')
        activity_instance.start_time = data.get('start_time')
        activity_instance.end_time = data.get('end_time')
        activity_instance.productive = data.get('productive')
        activity_instance.category = category
        activity_instance.save()
        
        return activity_instance
