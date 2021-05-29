from django.contrib.auth import get_user_model, authenticate
from knox.serializers import UserSerializer
from rest_framework import serializers

USER = get_user_model()


class LoginSerializer(UserSerializer):
    groups = serializers.SerializerMethodField()

    class Meta:
        model = USER
        fields = ['email', 'display_name', 'first_name', 'middle_name', 'last_name', 'groups', 'current_address',
                  'gender', 'birthdate', 'created_at', 'updated_at']

    def validate(self, attrs):
        USER.objects.get(email=attrs['email'])
        if USER.DoesNotExist:
            raise serializers.ValidationError({'detail': 'User does not exist'})
        return attrs

    @staticmethod
    def get_groups(obj):
        return obj.groups.all().values_list('name', flat=True)


class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(label="Username")
    password = serializers.CharField(
        label="Password",
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            try:
                USER.objects.get(email=attrs['username'])
            except USER.DoesNotExist:
                raise serializers.ValidationError({'detail': "User doesn't exist. Please enter correct username"})
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)

            if not user:
                msg = 'Please enter correct username or password.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
