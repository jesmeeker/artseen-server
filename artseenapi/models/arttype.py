from django.db import models

class ArtType(models.Model):
    label = models.CharField(max_length=50)
    subtypes = models.ManyToManyField("SubType", through="artsubrelationship", related_name='subtypes_of_arttype')