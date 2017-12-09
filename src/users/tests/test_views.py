from django.contrib.auth import get_user_model
from django.urls import reverse
from mixer.backend.django import mixer

from rest_framework.test import APIRequestFactory

from users.tests.fixtures import (
    new_user_info, 
    json_user_with_details, 
    json_user_with_details_with_one_null_detail, 
    json_user_no_details
)
from users.models import Details
from users.views import UserViewSet

import pytest
import json

pytestmark = pytest.mark.django_db
User = get_user_model()
factory = APIRequestFactory()
USERS_URI = 'api/users' 


class TestUsersViews:

    def test_user_view(self):
        view = UserViewSet.as_view({'get': 'list'})
        request = factory.get(USERS_URI)
        response = view(request)

        assert response.status_code == 200

    def test_view_create_user_with_details(self, json_user_with_details, json_user_with_details_with_one_null_detail, json_user_no_details):
        # Create user with json details
        view = UserViewSet.as_view({'post': 'create'})
        request = factory.post(USERS_URI, data=json.dumps(json_user_with_details), content_type='application/json')
        response = view(request)
        
        # Check if all the attributes match and if password doesn't show
        assert response.status_code == 201
        assert response.data.get('id') 
        assert not response.data.get('password') 
        assert response.data.get('first_name') == json_user_with_details['first_name']
        assert response.data.get('last_name') == json_user_with_details['last_name']
        assert response.data.get('email') == json_user_with_details['email']
        assert response.data.get('first_name') == json_user_with_details['first_name']

        instances = User.objects.filter(
                        first_name=json_user_with_details['first_name'], 
                        last_name=json_user_with_details['last_name']).count()
        
        # Check if username is correct
        if instances != 1:
            assert response.data.get('username') == '{}{}-{}'.format(json_user_with_details['first_name'], json_user_with_details['last_name'], instances)
        else:
            assert response.data.get('username') == '{}{}'.format(json_user_with_details['first_name'], json_user_with_details['last_name'])

        # Check details 
        assert response.data.get('details', {}).get('country') == json_user_with_details['details']['country']
        assert response.data.get('details', {}).get('goal') == json_user_with_details['details']['goal']
        assert response.data.get('details', {}).get('mobile_number') == json_user_with_details['details']['mobile_number']

        # Create another user with one detail as null
        request = factory.post(USERS_URI, data=json.dumps(json_user_with_details_with_one_null_detail), content_type='application/json')
        response = view(request)

        # Assert new user exists but it goal is empty while other details are the same
        assert response.status_code == 201
        assert response.data.get('id')
        assert not response.data.get('details', {}).get('goal') 
        assert response.data.get('details', {}).get('country') == json_user_with_details_with_one_null_detail['details']['country']
        assert response.data.get('details', {}).get('mobile_number') == json_user_with_details_with_one_null_detail['details']['mobile_number']
            
        # Create another user with no details
        request = factory.post(USERS_URI, data=json.dumps(json_user_no_details), content_type='application/json')
        response = view(request)
        
        # Assert it exists and has no details 
        assert response.status_code == 201
        assert response.data.get('id') 
        assert response.data.get('details')

    def test_view_list_and_retrieve_users(self, new_user_info, json_user_no_details):
        # Populate the database
        new_user = User.objects.create_user(
            first_name=new_user_info['first_name'],
            last_name=new_user_info['last_name'],
            email=new_user_info['email'],
            country=new_user_info['country'],
            mobile_number=new_user_info['mobile_number'],
            goal=new_user_info['goal'],
            password=new_user_info['password']
        )

        # Create another user via posting data
        post_view = UserViewSet.as_view({'post': 'create'})
        post_request = factory.post(USERS_URI, data=json.dumps(json_user_no_details), content_type='application/json')
        post_response = post_view(post_request)

        # Assert it was created
        assert post_response.status_code == 201
        assert post_response.data.get('id') 
        assert post_response.data.get('email') == json_user_no_details['email']
        assert post_response.data.get('details')
        
        # List all users and make sure there are 2, one populated by the db and one from posted data
        get_view = UserViewSet.as_view({'get': 'list'})
        get_request = factory.get(USERS_URI)
        get_response = get_view(get_request)

        assert get_response.status_code == 200
        assert len(get_response.data) == 2
        # Make sure they are users with id's and the same emails
        assert get_response.data[0].get('id')
        assert get_response.data[0].get('email') == new_user_info['email']
        assert get_response.data[1].get('id')
        assert get_response.data[1].get('email') == json_user_no_details['email']

        # Retrieve the user populated from teh database
        retrieve_view = UserViewSet.as_view({'get': 'retrieve'})
        retrieve_request = factory.get(USERS_URI+'/{}'.format(new_user.id))
        retrieve_response = retrieve_view(retrieve_request, pk=new_user.id)

        assert retrieve_response.status_code == 200
        assert retrieve_response.data.get('id') == new_user.id
        assert retrieve_response.data.get('email') == new_user.email

    def test_view_update_user(self, new_user_info, json_user_with_details, json_user_no_details):
        # Populate the database
        new_user = User.objects.create_user(
            first_name=new_user_info['first_name'],
            last_name=new_user_info['last_name'],
            email=new_user_info['email'],
            country=new_user_info['country'],
            mobile_number=new_user_info['mobile_number'],
            goal=new_user_info['goal'],
            password=new_user_info['password']
        )

        # Assert user was created with same fields
        assert new_user.id
        assert new_user.first_name == new_user_info['first_name']
        assert new_user.last_name == new_user_info['last_name']
        assert new_user.email == new_user_info['email']
        assert new_user.password != new_user_info['password']
        assert new_user.details.country == new_user_info['country']
        assert new_user.details.mobile_number == new_user_info['mobile_number']
        assert new_user.details.goal == new_user_info['goal']

        # Update the user with new_user.id
        view = UserViewSet.as_view({'put': 'update'})
        request = factory.put(USERS_URI+'/{}'.format(new_user.id), data=json.dumps(json_user_with_details), content_type='application/json')
        response = view(request, pk=new_user.id)
        
        # Get User with the same new_user.id
        edited_user = User.objects.get(id=new_user.id)

        # Assert response is the same as the fixture value which is also 
        # the same with the newly created and edited user
        assert response.data.get('id') == edited_user.id
        assert response.data.get('first_name') == json_user_with_details['first_name'] == edited_user.first_name
        assert response.data.get('last_name') == json_user_with_details['last_name'] == edited_user.last_name
        assert response.data.get('email') == json_user_with_details['email'] == edited_user.email
        assert response.data.get('details', {}).get('country') == json_user_with_details['details']['country'] == edited_user.details.country
        assert response.data.get('details', {}).get('mobile_number') == json_user_with_details['details']['mobile_number'] == edited_user.details.mobile_number
        assert response.data.get('details', {}).get('goal') == json_user_with_details['details']['goal'] == edited_user.details.goal

        # Edit the same user again but this time removing the details
        view = UserViewSet.as_view({'put': 'update'})
        request = factory.put(USERS_URI+'/{}'.format(new_user.id), data=json.dumps(json_user_no_details), content_type='application/json')
        response = view(request, pk=new_user.id)
        
        edited_user = User.objects.get(id=new_user.id)

        # Assert response is the same as the fixture value which is also 
        # the same with the newly created and edited user but having no details
        assert response.data.get('id') == edited_user.id
        assert response.data.get('first_name') == json_user_no_details['first_name'] == edited_user.first_name
        assert response.data.get('last_name') == json_user_no_details['last_name'] == edited_user.last_name
        assert response.data.get('email') == json_user_no_details['email'] == edited_user.email
        assert response.data.get('details')
        assert not response.data.get('details', {}).get('country')
        assert not response.data.get('details', {}).get('goal')
        assert not response.data.get('details', {}).get('mobile_number')
        
    def test_view_delete_user(self, new_user_info):
        new_user = User.objects.create_user(
            first_name=new_user_info['first_name'],
            last_name=new_user_info['last_name'],
            email=new_user_info['email'],
            country=new_user_info['country'],
            mobile_number=new_user_info['mobile_number'],
            goal=new_user_info['goal'],
            password=new_user_info['password']
        )

        # Delete the user with new_user.id
        view = UserViewSet.as_view({'delete': 'destroy'})
        request = factory.delete(USERS_URI+'/{}'.format(new_user.id))
        response = view(request, pk=new_user.id)

        assert response.status_code == 204
        assert User.objects.filter(id=new_user.id).count() == 0
        assert Details.objects.filter(user=new_user).count() == 0
        



