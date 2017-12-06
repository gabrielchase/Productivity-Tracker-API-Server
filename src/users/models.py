from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractUser,)


class BaseUserManager(BaseUserManager):

    def create_user(self, first_name, last_name, email, country=None, mobile_number=None, goal=None, password=None,):

        if not email:
            raise ValueError('Users must register an email address')

        if self.model.objects.filter(email=email).first():
            raise ValueError('Email address is already taken')

        new_user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=email
        )

        new_user.set_password(password)
        new_user.set_username()
        new_user.save(using=self._db)

        if new_user and (country or goal or mobile_number):
            new_user_details = Details.objects.create(
                user=new_user,
                country=country,
                goal=goal,
                mobile_number=mobile_number
            )
            new_user_details.save()

        return new_user


class BaseUser(AbstractUser):

    email = models.EmailField(max_length=255, unique=True, null=False)

    objects = BaseUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # removes email from REQUIRED_FIELDS

    def get_full_name(self):
        return '{}, {}'.format(self.last_name, self.first_name)

    def get_short_name(self):
        return self.username

    def set_username(self):
        instances = BaseUser.objects.filter(first_name=self.first_name, last_name=self.last_name).count()
        print("There are {} instances of '{} {}'".format(instances, self.first_name, self.last_name))
        
        if instances:
            print("Appending '-{}' to new_user's username".format(instances+1))
            self.username =  '{}{}-{}'.format(self.first_name, self.last_name, instances+1)
        else:
            self.username =  '{}{}'.format(self.first_name, self.last_name)
        
        print('Username of {} {}: {}'.format(self.first_name, self.last_name, self.username))
        self.save()

    def __str__(self):
        return '({}, {}, {}, {}, {})'.format(self.id, self.first_name, self.last_name, self.email, self.username)


class Details(models.Model):

    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE, primary_key=True)
    country = models.CharField(max_length=255, null=True)
    goal = models.TextField(null=True)
    mobile_number = models.CharField(max_length=255, null=True)

    def __str__(self):
        return str(self.user)
