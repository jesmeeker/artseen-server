from django.db import models

class PieceSubType(models.Model):
    piece = models.ForeignKey("Piece", on_delete=models.CASCADE, related_name='pieces_with_subtype')
    subtype = models.ForeignKey("SubType", on_delete=models.SET_NULL, related_name='subtypes_of_a_piece')