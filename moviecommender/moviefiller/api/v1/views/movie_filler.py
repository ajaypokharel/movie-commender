from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from moviecommender.commons.mixins.viewsets import ListRetrieveCreateViewSetMixin
from moviecommender.moviefiller.api.v1.serializers.apply import MovieFillerSerializer
from moviecommender.moviefiller.models import MovieFiller
from moviecommender.permissions.permissions import IsAdminUser, IsLoggedIn


class MovieFillerViewSet(ListRetrieveCreateViewSetMixin):
    lookup_field = 'uuid'
    lookup_url_kwarg = 'uuid'
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_queryset(self):
        return MovieFiller.objects.all()

    def get_permissions(self):
        if self.action in ['create']:
            return [IsAdminUser()]
        return [IsLoggedIn()]

    def get_serializer_class(self):
        return MovieFillerSerializer
