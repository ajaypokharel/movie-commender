import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django

django.setup()

from django.contrib.auth.models import Group
from moviecommender.permissions.constants import COMMON_USER, MOVIE_FILLER, ADMIN


GROUPS = [ADMIN, MOVIE_FILLER, COMMON_USER]

for group in GROUPS:
    new_group, _ = Group.objects.get_or_create(name=group)
