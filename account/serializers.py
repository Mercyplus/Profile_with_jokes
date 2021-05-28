from rest_framework import serializers
from .models import *


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class JokesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jokes
        fields = '__all__'
