from django.db import models

from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser,)


class User(AbstractBaseUser):

    first_name = models.CharField(max_length=255, unique=False, null=True)
    last_name = models.CharField(max_length=255, unique=False, null=True)
    email = models.EmailField(max_length=255, unique=True, null=False)
    slug = models.SlugField(unique=True)

    # objects = BaseUserManager()

    USERNAME_FIELD = 'email'

    def get_full_name(self):
        return '{}, {}'.format(self.last_name, self.first_naem)

    def get_short_name(self):
        return self.email

    def __str__(self):
        return '{}: {} | {}'.format(self.id, self.get_full_name(), self.email)

