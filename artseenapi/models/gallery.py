from django.db import models

class Gallery(models.Model):
    name = models.CharField(max_length=300)
    address = models.CharField(max_length=300)
    phone = models.BigIntegerField()
    square_feet = models.BigIntegerField()
    rooms = models.IntegerField()
    city = models.ForeignKey("City", on_delete=models.CASCADE)