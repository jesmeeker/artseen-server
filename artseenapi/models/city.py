from django.db import models

class City(models.Model):
    label = models.CharField(max_length=50)