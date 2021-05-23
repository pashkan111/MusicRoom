from django.db.models import fields
from .models import Room
from rest_framework import serializers

class RoomSerialiser(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = '__all__'


class RoomCreateSerialiser(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = ('guest_can_pause', 'votes_to_skip')

class RoomUpdateSerialiser(serializers.ModelSerializer):
    code = serializers.CharField()
    class Meta:
        model = Room
        fields = ('guest_can_pause', 'votes_to_skip', 'code')