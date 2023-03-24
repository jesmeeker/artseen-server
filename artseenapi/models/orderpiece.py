from django.db import models


class OrderPiece(models.Model):
    order = models.ForeignKey("Order", on_delete=models.DO_NOTHING, related_name="lineitems")
    piece = models.ForeignKey("Piece", on_delete=models.DO_NOTHING, related_name="lineitems")
