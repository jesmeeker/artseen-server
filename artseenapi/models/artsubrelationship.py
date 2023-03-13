from django.db import models

class ArtSubRelationship(models.Model):
    arttype = models.ForeignKey("ArtType", on_delete=models.CASCADE)
    subtype = models.ForeignKey("SubType", null=True, on_delete=models.SET_NULL)