from django.db import models
from django.contrib.auth.models import User


class PieceFavorites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_who_favorited_piece')
    piece = models.ForeignKey("Piece", null=True, on_delete=models.CASCADE, related_name='favorited_piece')