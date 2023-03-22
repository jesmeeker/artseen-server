from django.db import models
from django.contrib.auth.models import User


class ArtistFollows(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='artists_followers')
    artist = models.ForeignKey("Artist", null=True, on_delete=models.SET_NULL, related_name='artist_with_followers')