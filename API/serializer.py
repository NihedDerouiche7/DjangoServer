from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Input
from .models import Guide
from .models import Mygardin


class InputSerializerPOST(serializers.Serializer):
       X = serializers.CharField()
       Y = serializers.CharField()
       nbr_pas = serializers.IntegerField()
       def create(self, validated_data):
           return Input.objects.create(**validated_data)

class InputSerializerGET(serializers.Serializer):
       temperature = serializers.FloatField()
       humidity = serializers.FloatField()
       water = serializers.FloatField()
       created_at = serializers.DateTimeField()
       def create(self, validated_data):
           return Input.objects.create(**validated_data)


class GuideSerializer(serializers.Serializer):
       plantName = serializers.CharField()
       plantDisc = serializers.CharField()
       plantWaterUsage = serializers.FloatField()
       plantImageUrl = serializers.CharField()

       def create(self, validated_data):
           return Guide.objects.create(**validated_data)

class MygardinSerializer(serializers.Serializer):
       plantName = serializers.CharField()
       plantDisc = serializers.CharField()
       plantWaterUsage = serializers.FloatField()
       plantImageUrl = serializers.CharField()
       userId= serializers.IntegerField()

       def create(self, validated_data):
           return Mygardin.objects.create(**validated_data)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')