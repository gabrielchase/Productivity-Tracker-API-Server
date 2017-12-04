import pytest

from mixer.backend.django import mixer
from users.models import User
from users.tests.fixtures import new_user_info

# IMPORTANT: Allows tests to write into the database 
pytestmark = pytest.mark.django_db


class TestUser:

    def test_model_create_user(self, new_user_info):
        new_user = User.objects.create_user(
            new_user_info['first_name'],
            new_user_info['last_name'],
            new_user_info['email'],
            new_user_info['password']
        )

        expected_username = '{}{}'.format(new_user_info['first_name'], new_user_info['last_name'])
        
        assert new_user.id == 1, 'User instance should be created'
        assert new_user.first_name == new_user_info['first_name'], 'first_name should be the same'
        assert new_user.last_name == new_user_info['last_name'], 'last_name should be the same'
        assert new_user.email == new_user_info['email'], 'email should be the same'
        assert new_user.username == expected_username, 'username should be the same first_name + last_name'
        assert new_user.password != new_user_info['password'], 'password is hashed'

        assert new_user.get_full_name() == '{}, {}'.format(new_user.last_name, new_user.first_name)
        assert new_user.get_short_name() == new_user.username
        assert str(new_user) == '({}, {}, {}, {}, {})'.format(new_user.id, new_user.first_name, new_user.last_name, new_user.email, new_user.username)

    