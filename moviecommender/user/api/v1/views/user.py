from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from moviecommender.moviefiller.api.v1.serializers.apply import MovieFillerApplySerializer
from moviecommender.movies.api.v1.serializers.movie import MovieWatchListSerializer
from moviecommender.movies.models import MovieWatchList
from moviecommender.permissions.permissions import IsLoggedIn, IsAdminUser
from moviecommender.user.api.v1.serializers.password_reset import EmailOTPSerializer, OTPVerificationSerializer
from moviecommender.user.api.v1.serializers.user import UserRegisterationSerializer
from moviecommender.user.api.v1.serializers.password_change import PasswordChangeSerializer
from moviecommender.user.models import EmailOTP

USER = get_user_model()


class UserViewSet(ModelViewSet):
    lookup_field = 'username'
    lookup_url_kwarg = 'username'
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['first_name', 'last_name']
    ordering_fields = ['created_at', 'first_name']

    def get_queryset(self):
        if self.action in ['update', 'destroy', 'partial_update', 'me', 'change_password']:
            return USER.objects.filter(username=self.request.user.username)
        if self.action == 'watchlist':
            return MovieWatchList.objects.filter(watcher=self.request.user)
        if self.action in ['otp_send', 'verify_otp']:
            return USER.objects.exclude(is_verified=True)
        return USER.objects.all()

    def get_permissions(self):
        if self.action in ['update', 'destroy', 'partial_update', 'watchlist',
                           'me', 'moviefiller_apply', 'change_password', 'otp_send', 'verify_otp']:
            return [IsLoggedIn()]
        if self.action == 'assign_group':
            return [IsAdminUser()]
        return [AllowAny()]

    def get_serializer_class(self):
        if self.action == 'watchlist':
            return MovieWatchListSerializer
        if self.action == 'moviefiller_apply':
            return MovieFillerApplySerializer
        if self.action == 'change_password':
            return PasswordChangeSerializer
        if self.action == 'otp_send':
            return EmailOTPSerializer
        if self.action == 'verify_otp':
            return OTPVerificationSerializer
        return UserRegisterationSerializer

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        if self.action in ['update', 'partial_update']:
            kwargs['fields'] = ['email', 'first_name', 'middle_name', 'last_name', 'birthdate', 'current_address'
                                'gender', 'profile_picture', 'bio', 'fav_genre']
        if self.action in ['assign_group']:
            kwargs['fields'] = ['groups']
        return serializer_class(*args, **kwargs)

    @action(detail=False, methods=['get'])
    def watchlist(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['put'], url_path='assign-admin')
    def assign_group(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({'detail': "Group assigned successfully."})

    @action(detail=False, methods=['post'], url_path='apply-moviefiller')
    def moviefiller_apply(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def me(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='change-password')
    def change_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({'detail': 'Password Changed successfully!'})

    @action(detail=False, methods=['post'], url_path='otp-send')
    def otp_send(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'An email with an OTP code has been sent to your email'})

    @action(detail=False, methods=['post'], url_path='otp-verify')
    def verify_otp(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        otp = serializer.validated_data['otp']
        email = request.user.email
        EmailOTP.objects.filter(otp=otp, email=email).update(is_expired=True, is_verified=True)
        USER.objects.filter(email=email).update(is_verified=True)
        return Response({'detail': 'User Verified!'})
