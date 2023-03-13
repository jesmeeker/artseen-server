from django.db import models

class SubType(models.Model):
    label = models.CharField(max_length=50)