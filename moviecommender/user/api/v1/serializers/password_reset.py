from datetime import datetime, timedelta, timezone
import random

from django.core.mail import send_mail
from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework import serializers
from moviecommender.commons.serializers import DynamicFieldsModelSerializer
from moviecommender.user.models import EmailOTP


class EmailOTPSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = EmailOTP
        fields = ['created_at', 'updated_at', 'email', 'otp', 'is_expired', 'is_verified']
        read_only_fields = fields

    def create(self, validated_data):
        otp = random.randrange(100000, 999999)
        validated_data['otp'] = otp
        validated_data['email'] = self.request.user.email
        instance = super().create(validated_data)

        # send email
        email = instance.email
        subject = 'MovieCommender OTP'
        message = f'You requested an OTP verification. This is your OTP code: {otp}'
        from_email = 'support@moviecommender.com'
        recipient_list = [email, ]
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
        )

        return instance


class OTPVerificationSerializer(serializers.Serializer):
    otp = serializers.IntegerField(validators=[MinValueValidator(100000), MaxValueValidator(999999)])
    email = serializers.EmailField()

    def validate(self, attrs):
        user = EmailOTP.objects.filter(email=attrs['email'])
        if not user:
            raise serializers.ValidationError({'detail': 'The User with the email address does not exist. '
                                                         'Please enter valid email address'})
        try:
            user_otp = user.filter(otp=attrs['otp']).latest('created_at')
        except EmailOTP.DoesNotExist:
            raise serializers.ValidationError({'detail': 'OTP is invalid. Please enter correct OTP.'})
        if (user_otp.is_expired or
                (user_otp.created_at < datetime.now(timezone.utc) - timedelta(days=1))):
            raise serializers.ValidationError({'detail': 'The OTP has already expired.'})
        return attrs

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
