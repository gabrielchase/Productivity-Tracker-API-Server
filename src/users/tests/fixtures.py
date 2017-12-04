import pytest

from mixer.backend.django import mixer

from users.tests.utils import generate_random_password


@pytest.fixture
def new_user_info():
    
    return {
        'first_name': mixer.faker.first_name(),
        'last_name': mixer.faker.last_name(),
        'email': mixer.faker.email(),
        'password': generate_random_password()
    }
    

