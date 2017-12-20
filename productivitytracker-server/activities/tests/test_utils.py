from django.test import TestCase
from mixer.backend.django import mixer

from activities.models import Category
from activities.utils import handle_activity_category

import pytest
pytestmark = pytest.mark.django_db



class TestActivitiesUtils(TestCase):

    def setUp(self):
        Category.objects.create(name='Work')
        Category.objects.create(name='School')
        Category.objects.create(name='House')
        Category.objects.create(name='Exercise')        

    def test_handle_activity_category(self):
        categories = Category.objects.all()
        
        assert categories.count() == 4
        assert categories[0].id
        assert categories[0].name == 'Work'
        assert categories[1].id
        assert categories[1].name == 'School'
        assert categories[2].id
        assert categories[2].name == 'House'
        assert categories[3].id
        assert categories[3].name == 'Exercise'

        category_name = '{} {}'.format(mixer.faker.genre(), mixer.faker.genre())
        category = handle_activity_category(category_name)

        # Create new category if there is a different name
        categories = Category.objects.all()
        assert categories.count() == 5
        assert categories[4] == category
        assert categories[4].name == category_name.lower().title()

        # Don't create a new category of the given string 
        # if it already exists in `Category`
        bad_string = 'wOrK'
        category = handle_activity_category(bad_string)
        assert category.name == 'Work'
        assert Category.objects.all().count() == 5

        bad_string = 'eXerCiSE'
        category = handle_activity_category(bad_string)
        assert category.name == 'Exercise'
        assert Category.objects.all().count() == 5

        # Create new category if there is a different name
        bad_string = 'doInG hoMeWork'
        category = handle_activity_category(bad_string)
        assert category.name == 'Doing Homework'
        assert Category.objects.all().count() == 6
