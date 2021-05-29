import uuid

from django.contrib.auth import login, get_user_model
from knox.auth import TokenAuthentication
from knox.views import LoginView
from rest_framework.compat import coreapi, coreschema
from rest_framework.permissions import AllowAny
from rest_framework.schemas import ManualSchema

from ..serializers.login import AuthTokenSerializer

USER = get_user_model()


class KnoxLoginView(LoginView):
    permission_classes = (AllowAny, )
    authentication_classes = [TokenAuthentication, ]
    serializer_class = AuthTokenSerializer
    schema = ManualSchema(
        fields=[
            coreapi.Field(
                name="username",
                required=True,
                location='form',
                schema=coreschema.String(
                    title="Username",
                    description="Valid username for authentication",
                ),
            ),
            coreapi.Field(
                name="password",
                required=True,
                location='form',
                schema=coreschema.String(
                    title="Password",
                    description="Valid password for authentication",
                ),
            ),
        ],
        encoding="application/json",
    )

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super().post(request, format=None)
