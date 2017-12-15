from django.utils import timezone
from mixer.backend.django import mixer
from datetime import timedelta

import pytest
import random
import pytz


def return_bool():
    val = random.uniform(0, 1)
    
    if val:
        return True
    else:
        return False

@pytest.fixture
def new_activity_info():
    return {
        'name': mixer.faker.genre(),
        'description': mixer.faker.text(),
        'start_time': timezone.now(),
        'end_time': timezone.now() + timedelta(hours=1),
        'productive': return_bool(),
        'category': mixer.faker.genre()
    }
