from django.urls import path
from rest_framework.routers import DefaultRouter

from .v1.views.apply import MovieFillerApplyViewSet
from .v1.views.movie_filler import MovieFillerViewSet

r = DefaultRouter()

r.register('movie-filler', MovieFillerViewSet, basename='movie-filler')
r.register('apply', MovieFillerApplyViewSet, basename='apply')

urlpatterns = r.urls
