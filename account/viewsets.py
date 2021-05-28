from rest_framework import viewsets, permissions
from .serializers import *


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    permissions_classes = [
        permissions.AllowAny
    ]
    serializer_class = ProfileSerializer


class JokesViewSet(viewsets.ModelViewSet):
    queryset = Jokes.objects.all()
    permissions_classes = [
        permissions.AllowAny
    ]
    serializer_class = JokesSerializer
