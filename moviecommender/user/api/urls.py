from rest_framework.routers import DefaultRouter

from moviecommender.user.api.v1.views.user import UserViewSet

app_name = 'user'

r = DefaultRouter()

r.register('user', UserViewSet, basename='users')

urlpatterns = r.urls