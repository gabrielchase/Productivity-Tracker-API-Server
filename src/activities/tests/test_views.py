from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.serializers.json import DjangoJSONEncoder
from mixer.backend.django import mixer
from rest_framework.test import APIRequestFactory

from users.tests.utils import get_jwt_header
from users.tests.fixtures import (new_user_info, other_new_user_info)
from activities.models import (Category, Activity)
from activities.views import ActivityViewSet
from activities.utils import handle_activity_category
from activities.tests.fixtures import new_activity_info

import pytest
import json

pytestmark = pytest.mark.django_db
User = get_user_model()
factory = APIRequestFactory()
ACTIVITIES_URI = 'api/activities' 


class TestActivitiesViews:

    def test_view_activity_permissions(self, new_user_info, new_activity_info):
        # Create first user
        User.objects.create_user(
            first_name=new_user_info['first_name'],
            last_name=new_user_info['last_name'],
            email=new_user_info['email'],
            country=new_user_info['country'],
            mobile_number=new_user_info['mobile_number'],
            goal=new_user_info['goal'],
            password=new_user_info['password']
        )

        # Make datetimes strings and create new category
        new_activity_info['start_time'] = str(new_activity_info['start_time'])
        new_activity_info['end_time'] = str(new_activity_info['end_time'])
        new_activity_info['category']['name'] = handle_activity_category(new_activity_info['category']['name']).name

        view = ActivityViewSet.as_view({'post': 'create'})
        request = factory.post(
            ACTIVITIES_URI, 
            data=json.dumps(new_activity_info), 
            HTTP_AUTHORIZATION=get_jwt_header(new_user_info['email'], new_user_info['password']),
            content_type='application/json')
        response = view(request)

        activity_id = response.data.get('id')
        
        assert response.status_code == 201
        assert activity_id
        assert response.data.get('name') == new_activity_info['name']
        assert response.data.get('description') == new_activity_info['description']
        assert response.data.get('start_time') == str(new_activity_info['start_time'].replace(' ', 'T').split('+')[0]+'Z')
        assert response.data.get('end_time') == str(new_activity_info['end_time'].replace(' ', 'T').split('+')[0]+'Z')
        assert response.data.get('user_details', {}).get('id')
        assert response.data.get('user_details', {}).get('email') == new_user_info['email']
        assert response.data.get('category', {}).get('name') == new_activity_info['category']['name']

        onui = other_new_user_info()
        User.objects.create_user(
            first_name=onui['first_name'],
            last_name=onui['last_name'],
            email=onui['email'],
            country=onui['country'],
            mobile_number=onui['mobile_number'],
            goal=onui['goal'],
            password=onui['password']
        )

        # u2 can't GET created activity 
        bad_retrieve_view = ActivityViewSet.as_view({'get': 'retrieve'})
        bad_retrieve_request = factory.get(
            ACTIVITIES_URI+'/{}'.format(activity_id), 
            HTTP_AUTHORIZATION=get_jwt_header(onui['email'], onui['password'])
        )
        bad_retrieve_response = view(bad_retrieve_request, pk=activity_id)

        assert bad_retrieve_response.status_code == 405

        # u2 can't PUT created activity 
        edited_activity_info = new_activity_info
        edited_activity_info['name'] = 'slkdjfalsdf'
        edited_activity_info['description'] = 'slkdjfalsdf'

        bad_put_view = ActivityViewSet.as_view({'put': 'update'})
        bad_put_request = factory.put(
            ACTIVITIES_URI+'/{}'.format(activity_id), 
            data=json.dumps(edited_activity_info), 
            content_type='application/json',
            HTTP_AUTHORIZATION=get_jwt_header(onui['email'], onui['password'])
        )
        response = view(bad_put_request, pk=activity_id)
        
        assert response.status_code == 405

        # u2 can't DELETE created activity 
        bad_delete_view = ActivityViewSet.as_view({'delete': 'destroy'})
        bad_delete_request = factory.delete(
            ACTIVITIES_URI+'/{}'.format(activity_id),
            HTTP_AUTHORIZATION=get_jwt_header(onui['email'], onui['password'])
        )
        bad_delete_response = view(bad_delete_request, pk=activity_id)

        assert response.status_code == 405
