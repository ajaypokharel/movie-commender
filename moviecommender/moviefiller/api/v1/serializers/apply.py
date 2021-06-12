from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers

from moviecommender.commons.constants import MOVIE_FILLER
from moviecommender.commons.serializers import DynamicFieldsModelSerializer
from moviecommender.moviefiller.models import MovieFiller, MovieFillerApply
from moviecommender.user.api.v1.serializers.user import UserRegisterationSerializer

USER = get_user_model()


class MovieFillerSerializer(DynamicFieldsModelSerializer):
    filler = UserRegisterationSerializer(fields=['email', 'display_name', 'current_address', 'profile_picture'],
                                         read_only=True)

    class Meta:
        model = MovieFiller
        fields = ['uuid', 'filler', 'movies_filled', 'level']
        read_only_fields = fields

    def get_fields(self):
        fields = super().get_fields()
        view = self.context.get('view')
        if view and view.action == 'create':
            fields['filler'] = serializers.SlugRelatedField(slug_field='username', queryset=USER.objects.all())
        return fields

    @staticmethod
    def validate_filler(filler):
        if MovieFiller.objects.filter(filler=filler).exists():
            raise serializers.ValidationError({'detail': 'User is already a Movie Filler'})
        return filler

    def create(self, validated_data):
        user = validated_data['filler']
        instance = super().create(validated_data)
        user.groups.add(
            Group.objects.get(name=MOVIE_FILLER)
        )
        return instance


class MovieFillerApplySerializer(DynamicFieldsModelSerializer):
    applicant = UserRegisterationSerializer(fields=['email', 'first_name', 'last_name', 'display_name', 'birthdate',
                                                    'current_address', 'gender', 'profile_picture', 'bio', 'fav_genre'],
                                            read_only=True)

    class Meta:
        model = MovieFillerApply
        fields = ['uuid', 'applicant', 'reason', 'bio', 'status']
        read_only_fields = ['uuid', 'applicant', 'status']

    def get_extra_kwargs(self):
        extra_kwargs = super().get_extra_kwargs()
        view = self.context.get('view')
        if view and view.action in ['partial_update', 'update']:
            extra_kwargs['status'] = {
                'write_only': True
            }
        return extra_kwargs

    def create(self, validated_data):
        validated_data['applicant'] = self.request.user
        instance = super().create(validated_data)
        return instance

    def update(self, instance, validated_data):
        status = validated_data.get('status')
        if status == 'ACCEPTED':
            MovieFiller.objects.create(filler=self.request.user)
        return instance
