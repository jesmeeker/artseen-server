from django.db import models

class ArtSubRelationship(models.Model):
    arttype = models.ForeignKey("ArtType", on_delete=models.SET_NULL)
    subtype = models.ForeignKey("SubType", on_delete=models.SET_NULL)