from django.urls import path
from rest_framework.routers import DefaultRouter

from .v1.views.movie_filler import MovieFillerViewSet

r = DefaultRouter()

r.register('movie-filler', MovieFillerViewSet, basename='movie-filler')

urlpatterns = r.urls