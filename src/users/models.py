from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractUser,)


class BaseUserManager(BaseUserManager):

    def create_user(self, first_name, last_name, email, country=None, mobile_number=None, goal=None, password=None,):

        if not email:
            raise ValueError('Users must register an email address')

        if self.model.objects.filter(email=email).first():
            raise ValueError('Email address is already taken')

        username = '{}{}'.format(first_name, last_name)

        if self.model.objects.filter(username=username).first():
            instances = self.model.objects.filter(first_name=first_name, last_name=last_name).count()
            print("There are {} instances of '{} {}'. Appending {} to new_user's username"
                .format(instances, first_name, last_name, instances+1))
            username += '-{}'.format(instances + 1)
            print('Username created for new_user: {}'.format(username))

        new_user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username
        )

        new_user.set_password(password)
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

    def __str__(self):
        return '({}, {}, {}, {}, {})'.format(self.id, self.first_name, self.last_name, self.email, self.username)


class Details(models.Model):

    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE, primary_key=True)
    country = models.CharField(max_length=255, null=True)
    goal = models.TextField(null=True)
    mobile_number = models.CharField(max_length=255, null=True)

    def __str__(self):
        return str(self.user)
