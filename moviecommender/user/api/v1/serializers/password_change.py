from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password as dj_password_validation

from rest_framework import serializers

from moviecommender.commons.serializers import DynamicFieldsModelSerializer

USER = get_user_model()


class PasswordChangeSerializer(DynamicFieldsModelSerializer):
    old_password = serializers.CharField(max_length=128, write_only=True,
                                         style={'input_type': 'password'})
    new_password = serializers.CharField(max_length=128, write_only=True,
                                         style={'input_type': 'password'})
    repeat_password = serializers.CharField(max_length=128, write_only=True,
                                            style={'input_type': 'password'})

    class Meta:
        model = USER
        fields = ['old_password', 'new_password', 'repeat_password']

    def validate(self, attrs):
        user = self.request.user
        if self.request and self.request.method.lower() == 'post':
            if not user.check_password(attrs['old_password']):
                raise serializers.ValidationError({'old_password': "Entered password doesn't match with old password."})
            dj_password_validation(attrs['new_password'])
            if attrs['new_password'] != attrs['repeat_password']:
                raise serializers.ValidationError({'password': 'Passwords do not match.'})
        return attrs

    @staticmethod
    def validate_new_password(new_password):
        dj_password_validation(new_password)
        return new_password
