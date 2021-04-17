from django.db import models
from datetime import datetime    

# Create your models here.

class data_ny(models.Model):
    Time = models.CharField(max_length=50)
    temperature = models.IntegerField()
    dew_point = models.IntegerField()
    wind_speed = models.IntegerField()
    wind_gust = models.IntegerField()

class data_dl(models.Model):
    Time = models.CharField(max_length=50)
    temperature = models.IntegerField()
    dew_point = models.IntegerField()
    wind_speed = models.IntegerField()
    wind_gust = models.IntegerField()

class data_mum(models.Model):
    Time = models.CharField(max_length=50)
    temperature = models.IntegerField()
    dew_point = models.IntegerField()
    wind_speed = models.IntegerField()
    wind_gust = models.IntegerField()