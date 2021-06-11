from django.db import transaction
from rest_framework import serializers

from moviecommender.commons.serializers import DynamicFieldsModelSerializer
from moviecommender.moviefiller.models import MovieFiller
from moviecommender.movies.models import Movie, MovieWatchList
from moviecommender.user.api.v1.serializers.user import UserRegisterationSerializer
from moviecommender.user.constants import GENRE_CHOICES


class MovieSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Movie
        fields = ['slug', 'title', 'summary', 'cast', 'genre', 'director', 'writer', 'main_cast', 'mpaa_rating',
                  'cinematographer', 'prod_company', 'image', 'imdb_rating', 'rt_rating', 'metacritic_rating',
                  'language', 'release_date', 'runtime']
        read_only_fields = ['slug']

    def get_fields(self):
        fields = super().get_fields()
        if self.request and self.request.method.lower() == 'get':
            fields['image'] = serializers.URLField(source='get_image', read_only=True)
        if self.request and self.request.method.lower() == 'post':
            fields['genre'] = serializers.ListField(
                child=serializers.ChoiceField(choices=GENRE_CHOICES, allow_blank=True, allow_null=True),
                allow_empty=True
            )
            fields['director'] = serializers.ListField(max_length=100)
            fields['writer'] = serializers.ListField(max_length=100)
            fields['cast'] = serializers.ListField(max_length=100)
            fields['main_cast'] = serializers.ListField(max_length=100)
            fields['language'] = serializers.ListField(max_length=25)
        return fields

    @transaction.atomic()
    def create(self, validated_data):
        instance = super().create(validated_data)
        user = self.request.user
        if 'MOVIE_FILLER' in user.groups.values_list('name', flat=True):
            obj = MovieFiller.objects.get(filler=user)
            movies_filled = obj.movies_filled
            obj.movies_filled = movies_filled + 1
            obj.save()
        return instance


class MovieWatchListSerializer(DynamicFieldsModelSerializer):
    movie = MovieSerializer(fields=['title', 'summary', 'director', 'genre', 'director', 'writer'], read_only=True)
    watcher = UserRegisterationSerializer(fields=['display_name'], read_only=True)

    class Meta:
        model = MovieWatchList
        fields = ['movie', 'watcher']
        read_only_fields = ['movie', 'watcher']

    def create(self, validated_data):
        validated_data['movie'] = self.context.get('movie')
        validated_data['watcher'] = self.request.user
        instance = super().create(validated_data)
        return instance
