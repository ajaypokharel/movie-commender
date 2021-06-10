from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response

from moviecommender.commons.mixins.viewsets import ListRetrieveCreateViewSetMixin
from moviecommender.moviefiller.api.v1.serializers.apply import MovieFillerSerializer
from moviecommender.moviefiller.models import MovieFiller
from moviecommender.permissions.permissions import IsAdminUser, IsLoggedIn, IsMovieFiller


class MovieFillerViewSet(ListRetrieveCreateViewSetMixin):
    lookup_field = 'uuid'
    lookup_url_kwarg = 'uuid'
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_queryset(self):
        if self.action in ['my_profile']:
            return MovieFiller.objects.filter(filler=self.request.user)
        return MovieFiller.objects.all()

    def get_permissions(self):
        if self.action in ['create']:
            return [IsAdminUser()]
        if self.action in ['my_profile']:
            return [IsMovieFiller()]
        return [IsLoggedIn()]

    def get_serializer_class(self):
        return MovieFillerSerializer

    @action(detail=False, methods=['get'], url_path='my-profile')
    def my_profile(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
