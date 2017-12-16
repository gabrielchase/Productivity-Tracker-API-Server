from django.test import TestCase
from django.contrib.auth import get_user_model
from mixer.backend.django import mixer
from rest_framework.test import APIRequestFactory

from users.tests.utils import get_jwt_header
from users.tests.fixtures import new_user_info
from activities.models import (Category, Activity)
from activities.tests.fixtures import new_activity_info

import pytest
import json

pytestmark = pytest.mark.django_db
User = get_user_model()
factory = APIRequestFactory()
ACTIVITIES_URI = 'api/activities' 


class TestActivitiesViews(TestCase):

    def setUp(self):
        nui = new_user_info()
        u1 = User.objects.create_user(
            first_name=nui['first_name'],
            last_name=nui['last_name'],
            email=nui['email'],
            country=nui['country'],
            mobile_number=nui['mobile_number'],
            goal=nui['goal'],
            password=nui['password']
        )

        nui = new_user_info()
        u2 = User.objects.create_user(
            first_name=nui['first_name'],
            last_name=nui['last_name'],
            email=nui['email'],
            country=nui['country'],
            mobile_number=nui['mobile_number'],
            goal=nui['goal'],
            password=nui['password']
        )

        category_work = Category.objects.create(name='Work')
        category_school = Category.objects.create(name='School')

        nai = new_activity_info()

        Activity.objects.create(
            name=nai['name'],
            description=nai['description'],
            start_time=nai['start_time'],
            end_time=nai['end_time'],
            productive=nai['productive'],
            user=u1,
            category=category_work
        )

        nai = new_activity_info()

        Activity.objects.create(
            name=nai['name'],
            description=nai['description'],
            start_time=nai['start_time'],
            end_time=nai['end_time'],
            productive=nai['productive'],
            user=u1,
            category=category_school
        )

        nai = new_activity_info()

        Activity.objects.create(
            name=nai['name'],
            description=nai['description'],
            start_time=nai['start_time'],
            end_time=nai['end_time'],
            productive=nai['productive'],
            user=u2,
            category=category_work
        )

        nai = new_activity_info()

        Activity.objects.create(
            name=nai['name'],
            description=nai['description'],
            start_time=nai['start_time'],
            end_time=nai['end_time'],
            productive=nai['productive'],
            user=u2,
            category=category_school
        )

    def test_activity_permissions(self):

        print(User.objects.all())
        print(Category.objects.all())
        print(Activity.objects.all())

        assert 1 == 2