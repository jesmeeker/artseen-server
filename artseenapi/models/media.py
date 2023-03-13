from django.db import models

class Media(models.Model):
    label = models.CharField(max_length=50)
    artist = models.ForeignKey("Artist", null=True, on_delete=models.SET_NULL, related_name='artists_created_mediums')