from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import validate_password as dj_password_validation
from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers

from moviecommender.commons.constants import GROUP_CHOICES, COMMON_USER
from moviecommender.commons.serializers import DynamicFieldsModelSerializer
from moviecommender.user.constants import GENRE_CHOICES

USER = get_user_model()


class UserRegisterationSerializer(DynamicFieldsModelSerializer):
    repeat_password = serializers.CharField(
        max_length=128, write_only=True,
        style={'input_type': 'password'}
    )
    groups = serializers.ChoiceField(choices=GROUP_CHOICES, write_only=True, required=False)
    fav_genre = serializers.ListField(child=serializers.ChoiceField(choices=GENRE_CHOICES, required=False),
                                      required=False)

    class Meta:
        model = USER
        fields = ['username', 'email', 'first_name', 'middle_name', 'last_name', 'display_name', 'birthdate',
                  'current_address', 'gender', 'profile_picture', 'password', 'repeat_password', 'groups', 'created_at',
                  'updated_at', 'bio', 'fav_genre', 'is_verified']
        read_only_fields = ['username', 'display_name', 'created_at', 'updated_at', 'groups', 'is_verified']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def get_fields(self):
        fields = super().get_fields()
        if self.request and self.request.method.lower() == 'get':
            fields['profile_picture'] = serializers.URLField(source='get_profile_picture', read_only=True)
            fields['groups'] = serializers.SerializerMethodField()
        return fields

    @staticmethod
    def get_groups(obj):
        return obj.groups.all().values_list('name', flat=True)

    def validate(self, attrs):
        if self.request and self.request.method.lower() == 'post':
            dj_password_validation(attrs['password'])
            if attrs['password'] != attrs['repeat_password']:
                raise serializers.ValidationError({'password': 'Passwords do not match.'})
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        password = validated_data.pop('password')
        r_pass = validated_data.pop('repeat_password')
        group = validated_data.pop('groups', None)
        instance = super().create(validated_data)
        instance.set_password(password)
        instance.save()
        if group and group not in instance.groups.all().values_list('name', flat=True):
            instance.groups.clear()
            instance.groups.add(
                Group.objects.get(name__iexact=group)
            )
        else:
            instance.groups.add(
                Group.objects.get(name=COMMON_USER)
            )
        return instance
