from django.db import models
from django.contrib.auth.models import User

class Piece(models.Model):
    artist = models.ForeignKey("Artist", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=500, null=True)
    arttype = models.ForeignKey("ArtType", null=True, on_delete=models.SET_NULL, related_name='arttype_pieces')
    subtypes = models.ManyToManyField("SubType", through="piecesubtype", related_name='subtype_pieces')
    media = models.ForeignKey("Media", null=True, on_delete=models.SET_NULL, related_name='pieces_using_this_media')
    surface = models.ForeignKey("Surface", null=True, on_delete=models.SET_NULL, related_name='pieces_using_this_surface')
    length = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()
    weight = models.FloatField(null=True, blank=True)
    image_url = models.CharField(max_length=250)
    about = models.CharField(max_length=1000)
    available_purchase = models.BooleanField(default=False)
    available_show = models.BooleanField(default=False)
    will_ship = models.BooleanField(default=False)
    unique = models.BooleanField(default=True)
    quantity_available = models.IntegerField(null=True)
    price = models.FloatField(null=True)
    private = models.BooleanField(default=False)
    date_added = models.DateField(null=True, blank=True, auto_now=False, auto_now_add=True)
    likes = models.ManyToManyField(User, through="piecelikes", related_name='likes_of_piece')

    @property
    def creator(self):
        return self.__creator

    @creator.setter
    def creator(self, value):
        self.__creator = value

    @property
    def user_likes(self):
        return self.__user_likes

    @user_likes.setter
    def user_likes(self, value):
        self.__user_likes = value