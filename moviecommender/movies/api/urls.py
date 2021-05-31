from rest_framework.routers import DefaultRouter

from moviecommender.movies.api.v1.views.movie import MovieViewSet

app_name = 'movies'

r = DefaultRouter()

r.register('movies', MovieViewSet, basename='movies')

urlpatterns = r.urls
