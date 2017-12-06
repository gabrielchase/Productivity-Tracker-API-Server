import pytest

from mixer.backend.django import mixer

from users.tests.utils import generate_random_password


@pytest.fixture
def new_user_info():
    return {
        'first_name': mixer.faker.first_name(),
        'last_name': mixer.faker.last_name(),
        'email': mixer.faker.email(),
        'country': mixer.faker.country(),
        'mobile_number': mixer.faker.phone_number(),
        'goal': mixer.faker.text(),
        'password': generate_random_password()
    }
    
@pytest.fixture
def json_user_with_details():
    return {
        'first_name': mixer.faker.first_name(),
        'last_name': mixer.faker.last_name(),
        'email': mixer.faker.email(),
        'password': generate_random_password(),
        'details': {
            'country': mixer.faker.country(),
            'mobile_number': mixer.faker.phone_number(),
            'goal': mixer.faker.text()
        }
    }

@pytest.fixture
def json_user_with_details_with_one_null_detail():
    return {
        'first_name': mixer.faker.first_name(),
        'last_name': mixer.faker.last_name(),
        'email': mixer.faker.email(),
        'password': generate_random_password(),
        'details': {
            'country': mixer.faker.country(),
            'mobile_number': mixer.faker.phone_number(),
            'goal': None
        }
    }


@pytest.fixture
def json_user_no_details():
    return {
        'first_name': mixer.faker.first_name(),
        'last_name': mixer.faker.last_name(),
        'email': mixer.faker.email(),
        'password': generate_random_password(),
        'details': {
            'country': None,
            'mobile_number': None,
            'goal': None
        }
    }
    

