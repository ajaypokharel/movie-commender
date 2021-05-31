from django.contrib.auth import get_user_model
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet

from moviecommender.user.api.v1.serializers.user import UserRegisterationSerializer

USER = get_user_model()


class UserViewSet(ModelViewSet):
    lookup_field = 'username'
    lookup_url_kwarg = 'username'
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['first_name', 'last_name']
    ordering_fields = ['created_at', 'first_name']

    def get_queryset(self):
        if self.action in ['update', 'destroy', 'partial_update']:
            return USER.objects.filter(username=self.request.user.username)
        return USER.objects.all()

    def get_permissions(self):
        if self.action in ['update', 'destroy', 'partial_update']:
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_serializer_class(self):
        return UserRegisterationSerializer

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        if self.action in ['update', 'partial_update']:
            kwargs['fields'] = ['email', 'first_name', 'middle_name', 'last_name', 'birthdate', 'current_address'
                                'gender', 'profile_picture', 'bio', 'fav_genre']
        return serializer_class(*args, **kwargs)




