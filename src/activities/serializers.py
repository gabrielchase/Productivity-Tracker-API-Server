from rest_framework import serializers
from rest_framework.renderers import JSONRenderer

from django.contrib.auth import get_user_model
User = get_user_model()

from activities.models import (Activity, Category)
from activities.utils import handle_category_name

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

    def create(self, data):
        category_name = handle_category_name(data.pop('category', {}).get('name'))
        category = Category.objects.filter(name=category_name).first()

        if not category:
            category = Category.objects.create(name=category_name)

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
        