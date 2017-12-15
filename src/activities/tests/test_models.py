from django.contrib.auth import get_user_model
from mixer.backend.django import mixer

from users.tests.fixtures import new_user_info

from activities.models import (Activity, Category)
from activities.tests.fixtures import new_activity_info
from activities.utils import handle_activity_category

# IMPORTANT: Allows tests to write into the database 
import pytest
pytestmark = pytest.mark.django_db
User = get_user_model()


class TestActivitiesModels:

    def test_model_create_activity(self, new_activity_info, new_user_info):
        new_user = User.objects.create_user(
            first_name=new_user_info['first_name'],
            last_name=new_user_info['last_name'],
            email=new_user_info['email'],
            country=new_user_info['country'],
            mobile_number=new_user_info['mobile_number'],
            goal=new_user_info['goal'],
            password=new_user_info['password']
        )

        category = handle_activity_category(new_activity_info['category'])

        new_activity = Activity.objects.create(
            name=new_activity_info['name'],
            description=new_activity_info['description'],
            start_time=new_activity_info['start_time'],
            end_time=new_activity_info['end_time'],
            productive=new_activity_info['productive'],
            user=new_user,
            category=category
        )

        assert new_activity.id
        assert new_activity.name == new_activity_info['name']
        assert new_activity.description == new_activity_info['description']
        assert new_activity.start_time == new_activity_info['start_time']
        assert new_activity.end_time == new_activity_info['end_time']
        assert new_activity.productive == new_activity_info['productive']
        assert new_activity.user == new_user
        assert new_activity.category == category
