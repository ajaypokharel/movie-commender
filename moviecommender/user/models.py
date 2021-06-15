import os
import uuid
from urllib.parse import urljoin

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from config import settings
from moviecommender.commons.models import TimeStampModel
from moviecommender.user.constants import GENDER_CHOICES, GENRE_CHOICES
from moviecommender.user.manager import UserManager


def get_profile_picture_upload_path(_, filename):
    extension = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), extension)
    return os.path.join('user/profile-picture/', filename)


class User(TimeStampModel, AbstractUser):
    username_validator = UnicodeUsernameValidator()
    username = models.UUIDField(
        max_length=100,
        unique=True,
        validators=[username_validator],
        error_messages={
            'unique': 'A user with that username already exists.',
        },
        default=uuid.uuid4
    )
    email = models.EmailField(
        unique=True, max_length=50,
        error_messages={
            'unique': 'A user with that email already exists.',
        },
    )

    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50)
    birthdate = models.DateField(blank=True, null=True)
    current_address = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    profile_picture = models.ImageField(upload_to=get_profile_picture_upload_path, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    fav_genre = models.CharField(max_length=25, choices=GENRE_CHOICES, blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name', 'last_name']

    @property
    def display_name(self):
        return f"{self.first_name.capitalize()} {self.last_name.capitalize()}" if not self.middle_name \
            else f"{self.first_name.capitalize()} {self.middle_name.capitalize()} {self.last_name.capitalize()}"

    @property
    def get_profile_picture(self):
        if self.profile_picture:
            return urljoin(settings.BACKEND_URL, self.profile_picture.url)
        return urljoin(settings.BACKEND_URL, urljoin(settings.STATIC_URL, 'user/default_profile_picture.jpeg'))


class EmailOTP(TimeStampModel):
    email = models.EmailField()
    otp = models.PositiveIntegerField(validators=[MinValueValidator(100000), MaxValueValidator(999999)])
    is_expired = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
