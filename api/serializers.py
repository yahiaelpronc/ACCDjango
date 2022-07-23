from rest_framework import serializers
from .models import *


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Myuser
        fields = '__all__'


class VetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vet
        fields = ('username','profile_pic' ,'firstname','lastname','email','password','country','address','mobile','b_date',
        'active_status','face_link','active_link','specialization',)


class LocationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = locations
        fields = '__all__'


class MessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = '__all__'


class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = '__all__'
