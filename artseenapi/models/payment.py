from django.db import models
from .viewer import Viewer

class Payment(models.Model):

    merchant_name = models.CharField(max_length=25,)
    account_number = models.CharField(max_length=25)
    viewer = models.ForeignKey(Viewer, on_delete=models.DO_NOTHING, related_name="payment_types")
    expiration_date = models.DateField(default="0000-00-00",)
    create_date = models.DateField(default="0000-00-00",)
    zip_code = models.IntegerField()
