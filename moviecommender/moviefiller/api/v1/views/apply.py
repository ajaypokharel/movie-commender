from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response

from moviecommender.commons.constants import PENDING
from moviecommender.commons.mixins.viewsets import ListRetrieveUpdateViewSetMixin
from moviecommender.moviefiller.api.v1.serializers.apply import MovieFillerApplySerializer
from moviecommender.moviefiller.models import MovieFillerApply, MovieFiller
from moviecommender.permissions.permissions import IsAdminUser


class MovieFillerApplyViewSet(ListRetrieveUpdateViewSetMixin):
    lookup_field = 'uuid'
    lookup_url_kwarg = 'uuid'
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    serializer_class = MovieFillerApplySerializer

    def get_queryset(self):
        if self.action in ['update', 'partial_update']:
            return MovieFillerApply.objects.filter(status=PENDING)
        return MovieFillerApply.objects.all()

    def get_permissions(self):
        return [IsAdminUser()]

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        if self.action in ['update', 'partial_update']:
            kwargs['fields'] = ['status']
        return serializer_class(*args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({'detail': 'The status has been updated'})

