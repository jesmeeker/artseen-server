from django.db import models
from django.contrib.auth.models import User


class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.IntegerField()
    gallery = models.ForeignKey("Gallery", null=False, on_delete=models.CASCADE)
    city = models.ForeignKey("City", null=True, on_delete=models.SET_NULL, related_name='manager_in_the_city')

    @property
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'
