from rest_framework import serializers
from .models import *


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Myuser
        fields = '__all__'


class VetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vet
        fields = '__all__'


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


class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        fields = '__all__'


class SurgicalOperationsRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurgicalOperationsRequest
        fields = '__all__'


class SurgicalOperationsRequestUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurgicalOperationsRequest
        fields = ['status', ]


class SurgicalOperationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurgicalOperations
        fields = '__all__'


class ServiseRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiseRequest
        fields = '__all__'
