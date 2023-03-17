"""View module for handling requests about artists"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from artseenapi.models import Artist, City
from django.contrib.auth.models import User

class ArtistView(ViewSet):
    """Rare artist view"""

    def destroy(self, request, pk):
        artist = Artist.objects.get(pk=pk)
        artist.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, pk):
        """Handle GET requests for events

        Returns:
            Response -- JSON serialized events
        """
        try:
            artist = Artist.objects.get(pk=pk)

        except Artist.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ArtistSerializer(artist)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        """Handle GET requests to get all artists

        Returns:
            Response -- JSON serialized list of artists
        """
        artists = Artist.objects.all()

        if "user" in request.query_params:
            artists = artists.filter(user=request.auth.user)
        
        serializer = ArtistSerializer(artists, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk):
        """Handle ARTIST operations

        Returns
            Response -- JSON serialized game instance
        """
        try:
            city = City.objects.get(pk=request.data['city'])
        except City.DoesNotExist:
            return Response({'message': 'You sent an invalid city Id'}, status=status.HTTP_404_NOT_FOUND)

        artist_to_update = Artist.objects.get(pk=pk)
        artist_to_update.phone_number = request.data['phone']
        artist_to_update.bio = request.data['bio']
        artist_to_update.website = request.data['website']
        artist_to_update.image_url = request.data['image_url']
        artist_to_update.city = city
        artist_to_update.save()

        user_to_update = User.objects.get(user=request.auth.user)
        user_to_update.first_name = request.data['first_name']
        user_to_update.last_name = request.data['last_name']
        user_to_update.email = request.data['email']
        user_to_update.password = request.data['password']
        user_to_update.username = request.data['username']
        user_to_update.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for artists
    """

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'is_staff')

class CitySerializer(serializers.ModelSerializer):
    """JSON serializer for artists
    """

    class Meta:
        model = City
        fields = ('id', 'label')

class ArtistSerializer(serializers.ModelSerializer):
    """JSON serializer for artists
    """
    user = UserSerializer()
    city = CitySerializer()

    class Meta:
        model = Artist
        fields = ('id', 'user', 'phone_number', 'bio', 'website', 'image_url', 'city', 'staff')