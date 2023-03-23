"""Customer order model"""
from django.db import models
from .viewer import Viewer
from .payment import Payment


class Order(models.Model):
    viewer = models.ForeignKey(Viewer, on_delete=models.DO_NOTHING,)
    payment_type = models.ForeignKey(Payment, on_delete=models.DO_NOTHING, null=True)
    created_date = models.DateField(default="0000-00-00",)
