"""
v1 API url for swagger view
"""
from django.urls import path, include
from knox import views as knoxViews
from rest_framework.routers import DefaultRouter

from moviecommender.user.api.v1.views.login import KnoxLoginView

ROUTER = DefaultRouter()

# Place urlpatterns in alphabetical order
urlpatterns = [
    path('auth/login/', KnoxLoginView.as_view(), name='knox_login'),
    path('auth/logout/', knoxViews.LogoutView.as_view(), name='knox_logout'),
    path('movies/', include('moviecommender.movies.api.urls')),
    path('users/', include('moviecommender.user.api.urls')),

] + ROUTER.urls
