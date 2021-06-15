from rest_framework import serializers
from moviecommender.commons.serializers import DynamicFieldsModelSerializer
from moviecommender.user.models import EmailOTP


class EmailOTPSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = EmailOTP
        fields = ['created_at', 'updated_at', 'email', 'otp', 'is_expired', 'is_verified']
        read_only_fields = ['created_at', 'updated_at', 'otp', 'is_expired', 'is_verified']


class VerifyOTPSerializer(serializers.Serializer):
    otp = serializers.IntegerField()
