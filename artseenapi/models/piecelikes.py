from django.db import models
from django.contrib.auth.models import User


class PieceLikes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users_who_liked_piece')
    piece = models.ForeignKey("Piece", null=True, on_delete=models.CASCADE, related_name='piece_with_likes')