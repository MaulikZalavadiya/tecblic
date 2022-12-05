from django.urls import path, include
from rest_framework import routers
from custom_auth import api

router = routers.SimpleRouter()
router.register('auth', api.UserAuthViewSet, basename='auth')
router.register('users', api.UserViewSet, basename='users')

app_name = 'custom-auth'

urlpatterns = [
    path('', include(router.urls)),
]
