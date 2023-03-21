from django.db import models
from django.contrib.auth.models import User


class Viewer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.IntegerField()
    city = models.ForeignKey("City", null=True, on_delete=models.SET_NULL, related_name='viewers_in_the_city')

    @property
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'