from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from moviecommender.movies.api.v1.serializers.movie import MovieSerializer, MovieWatchListSerializer
from moviecommender.movies.models import Movie
from moviecommender.permissions.permissions import IsMovieFiller


class MovieViewSet(ModelViewSet):
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'director', 'cast', 'genre', 'slug']
    ordering_fields = ['created_at', 'first_name']

    def get_queryset(self):
        return Movie.objects.all()

    def get_permissions(self):
        if self.action == 'add_to_watchlist':
            return [IsAuthenticated()]
        return [IsMovieFiller()]

    def get_serializer_class(self):
        if self.action == 'add_to_watchlist':
            return MovieWatchListSerializer
        return MovieSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        lookup_url_kwargs = self.lookup_url_kwarg or self.lookup_field
        if self.action == 'add_to_watchlist':
            if lookup_url_kwargs in self.kwargs:
                context['movie'] = self.get_object()
        return context

    @action(detail=True, methods=['post'], url_path='add-to-watchlist')
    def add_to_watchlist(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'Movie added to watch list'}, status=status.HTTP_201_CREATED)