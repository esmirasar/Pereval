from django.db import models


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
    status = models.CharField(max_length=10)


class Coords(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    height = models.IntegerField()


class Level(models.Model):
    winter = models.CharField(max_length=2)
    summer = models.CharField(max_length=2)
    autumn = models.CharField(max_length=2)
    spring = models.CharField(max_length=2)


class Images(models.Model):
    data = models.ImageField()
    title = models.CharField(max_length=100)
    pereval = models.ForeignKey('Pereval', on_delete=models.CASCADE, )
