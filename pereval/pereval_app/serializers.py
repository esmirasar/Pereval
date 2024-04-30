from rest_framework import serializers
from .models import User, Coords, Pereval, Level, Images


class UserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    fam = serializers.CharField(max_length=50)
    name = serializers.CharField(max_length=50)
    otc = serializers.CharField(max_length=50)
    phone = serializers.CharField(max_length=50)

    def create(self, validated_data):
        return User.objects.create(**validated_data)


class PerevalSerializer(serializers.Serializer):
    beauty_title = serializers.CharField(max_length=30)
    title = serializers.CharField(max_length=50)
    other_titles = serializers.CharField(max_length=50)
    connect = serializers.CharField(max_length=50, allow_null=True, allow_blank=True)
    add_time = serializers.DateTimeField()
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    coords = serializers.PrimaryKeyRelatedField(queryset=Coords.objects.all())
    level = serializers.PrimaryKeyRelatedField(queryset=Level.objects.all())

    def create(self, validated_data):
        return Pereval.objects.create(**validated_data)


class CoordsSerializer(serializers.Serializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    height = serializers.IntegerField()

    def create(self, validated_data):
        return Coords.objects.create(**validated_data)


class LevelSerializer(serializers.Serializer):
    winter = serializers.CharField(max_length=2, allow_null=True, allow_blank=True)
    summer = serializers.CharField(max_length=2, allow_null=True, allow_blank=True)
    autumn = serializers.CharField(max_length=2, allow_null=True, allow_blank=True)
    spring = serializers.CharField(max_length=2, allow_null=True, allow_blank=True)

    def create(self, validated_data):
        return Level.objects.create(**validated_data)


class ImagesSerializer(serializers.Serializer):
    data = serializers.ImageField()
    title = serializers.CharField(max_length=100)
    pereval = serializers.PrimaryKeyRelatedField(queryset=Pereval.objects.all())

    def create(self, validated_data):
        return Images.objects.create(**validated_data)
