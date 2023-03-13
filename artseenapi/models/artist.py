from django.db import models
from django.contrib.auth.models import User


class Artist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.BigIntegerField(max_length=10)
    bio = models.CharField(max_length=1000)
    website = models.CharField(max_length=250, null=True)
    image_url = models.CharField(max_length=250)
    city = models.ForeignKey("City", on_delete=models.SET_NULL, related_name='artists_in_the_city')

    @property
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'