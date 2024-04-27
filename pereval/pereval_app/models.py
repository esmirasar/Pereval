from django.db import models
from .category import CATEGORY_CHOICES, LEVEL_CHOICES


class User(models.Model):
    email = models.EmailField(unique=True)
    fam = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    otc = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)


class Pereval(models.Model):
    beauty_title = models.CharField(max_length=30)
    title = models.CharField(max_length=50)
    other_titles = models.CharField(max_length=50)
    connect = models.CharField(max_length=50)
    add_time = models.DateTimeField()
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    coords = models.ForeignKey('Coords', on_delete=models.CASCADE)
    level = models.ForeignKey('Level', on_delete=models.CASCADE)


class Coords(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    height = models.IntegerField()


class Level(models.Model):
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    difficulty_level = models.CharField(max_length=2, choices=LEVEL_CHOICES)


class Image(models.Model):
    image = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100)
