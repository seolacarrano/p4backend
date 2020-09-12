from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)

# set JWT setting
from rest_framework_jwt.settings import api_settings

# set JWT payload
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

# Create your models here.
class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None, first_name=None, last_name=None):
        if username is None:
            raise TypeError("Users must have a username")
        if email is None:
            raise TypeError("Users must have an email address")

        # create a user object
        user = self.model(
            username=username,  # take username from parameter and inject to object
            email=self.normalize_email(email),   # make everything lower cases
            first_name=first_name,
            last_name=last_name,
            is_staff=False   # when users make a username, they're not staff
        )

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        if password is None:
            raise TypeError("Superusers must have a password")
        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True)      # db_index=True: username will act as index in database, make each user unique
    email = models.EmailField(db_index=True, unique=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True) # when a user is created for the first time, freeze that info
    updated_at = models.DateTimeField(auto_now=True)     # auto_now_add cannot be changed, auto_now can be changed

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']   # if I want to make last name required, I can do ['email', 'last_name']
    objects = UserManager()       # tells Django that UserManager class defined above should manage objects of this type

    def __str__(self):
        return self.username     # when a user is logged in,

    @property          # whenever you create a user dynamically, go and find this method so we can generate token for the specific user
    def token(self):
        return self._generate_jwt_token()      #_generate_jwt_token is private method

    def _generate_jwt_token(self):
        """
        Generates a JSON Web Token that stores this(self) or the current object
        user's instance and has an expiry data set to 60 days into the future
        """
        payload = jwt_payload_handler(self)
        token = jwt_encode_handler(payload)

        return token
