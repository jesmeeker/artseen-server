"""View module for handling requests about artists"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from artseenapi.models import Artist, City, ArtistFollows
from django.contrib.auth.models import User
from rest_framework.decorators import action
from django.db.models import Q



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
        follows = ArtistFollows.objects.all()
        follows = follows.filter(user=request.auth.user)    

        try:
            artist = Artist.objects.get(pk=pk)
            followers = follows.filter(Q(artist=artist))
            if followers:
                artist.follower = True
            else:
                artist.follower = False 

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

        for artist in artists:
            followers = ArtistFollows.objects.filter(Q(user_id=request.auth.user) & Q(artist=artist))
            if followers:
                artist.follower = True
            else:
                artist.follower = False

        serializer = ArtistSerializer(artists, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk):
        """Handle ARTIST operations

        Returns
            Response -- JSON serialized game instance
        """
        city_info = request.data['city']

        try:
            city = City.objects.get(pk=city_info['id'])
        except City.DoesNotExist:
            return Response({'message': 'You sent an invalid city Id'}, status=status.HTTP_404_NOT_FOUND)

        artist_to_update = Artist.objects.get(pk=pk)
        artist_to_update.phone_number = request.data['phone_number']
        artist_to_update.bio = request.data['bio']
        artist_to_update.website = request.data['website']
        artist_to_update.image_url = request.data['image_url']
        artist_to_update.city = city
        artist_to_update.save()

        user_info = request.data['user']

        user_to_update = User.objects.get(pk=request.auth.user_id)
        user_to_update.first_name = user_info['first_name']
        user_to_update.last_name = user_info['last_name']
        user_to_update.email = user_info['email']
        user_to_update.username = user_info['username']
        user_to_update.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post'], detail=True)
    def follow(self, request, pk):
        """Post request for a user to sign up for an event"""
        user = User.objects.get(id=request.auth.user_id)
        artist = Artist.objects.get(pk=pk)
        artist.followers.add(user)
        return Response({'message': 'User added'}, status=status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=True)
    def unfollow(self, request, pk):
        """Post request for a user to sign up for an event"""
    
        user = User.objects.get(id=request.auth.user_id)
        artist = Artist.objects.get(pk=pk)
        artist.followers.remove(user)
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for artists
    """

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username',)


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
        fields = ('id', 'user', 'full_name', 'phone_number',
                  'bio', 'website', 'image_url', 'city', 'follower')
