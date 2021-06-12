import os
import uuid
from urllib.parse import urljoin

from django.contrib.auth import get_user_model
from django.db import models

from config import settings
from moviecommender.commons.models import SlugModel, UUIDBaseModel
from moviecommender.user.constants import GENRE_CHOICES


USER = get_user_model()


def get_movie_picture_upload_path(_, filename):
    extension = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), extension)
    return os.path.join('movie/picture/', filename)


class Movie(SlugModel):
    title = models.CharField(max_length=250)
    summary = models.TextField(blank=True, null=True)
    cast = models.JSONField()
    genre = models.JSONField()
    director = models.JSONField()
    writer = models.JSONField()
    main_cast = models.JSONField(blank=True, null=True)
    mpaa_rating = models.CharField(max_length=12)
    cinematographer = models.CharField(max_length=100)
    prod_company = models.CharField(max_length=250, blank=True, null=True)
    image = models.ImageField(upload_to=get_movie_picture_upload_path, blank=True, null=True)
    imdb_rating = models.PositiveIntegerField(blank=True, null=True)
    rt_rating = models.PositiveIntegerField(blank=True, null=True)
    metacritic_rating = models.PositiveIntegerField(blank=True, null=True)
    language = models.JSONField(null=True, blank=True)
    release_date = models.DateField(blank=True, null=True)
    runtime = models.IntegerField(blank=True, null=True)

    @property
    def get_image(self):
        if self.image:
            return urljoin(settings.BACKEND_URL, self.image.url)
        return urljoin(settings.BACKEND_URL, urljoin(settings.STATIC_URL, 'movie/image.jpeg'))


class MovieWatchList(UUIDBaseModel):
    watcher = models.ForeignKey(USER, on_delete=models.CASCADE, related_name='movie_watcher')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie_watchlist')

