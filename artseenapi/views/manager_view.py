"""View module for handling requests about managers"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from artseenapi.models import Manager, City, Gallery
from django.contrib.auth.models import User
from django.db.models import Q


class ManagerView(ViewSet):
    """Rare artist view"""

    def destroy(self, request, pk):
        manager = Manager.objects.get(pk=pk)
        manager.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def list(self, request):
        """Handle GET requests for events

        Returns:
            Response -- JSON serialized events
        """
        managers = Manager.objects.all()

        if "user" in request.query_params:
            managers = managers.filter(user_id=request.auth.user_id)

        serializer = ManagerSerializer(managers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk):
        """Handle ARTIST operations

        Returns
            Response -- JSON serialized game instance
        """
        city_info = request.data['city']
        gallery_info = request.data['gallery']

        try:
            city = City.objects.get(pk=city_info['id'])
        except City.DoesNotExist:
            return Response({'message': 'You sent an invalid city Id'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            gallery = Gallery.objects.get(pk=gallery_info['id'])
        except Gallery.DoesNotExist:
            return Response({'message': 'You sent an invalid city Id'}, status=status.HTTP_404_NOT_FOUND)

        manager_to_update = Manager.objects.get(pk=pk)
        manager_to_update.phone_number = request.data['phone_number']
        manager_to_update.city = city
        manager_to_update.gallery = gallery
        manager_to_update.save()

        user_info = request.data['user']

        user_to_update = User.objects.get(pk=request.auth.user_id)
        user_to_update.first_name = user_info['first_name']
        user_to_update.last_name = user_info['last_name']
        user_to_update.email = user_info['email']
        user_to_update.username = user_info['username']
        user_to_update.save()

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


class GallerySerializer(serializers.ModelSerializer):
    """JSON serializer for artists
    """

    class Meta:
        model = Gallery
        fields = ('id', 'name')


class ManagerSerializer(serializers.ModelSerializer):
    """JSON serializer for artists
    """
    gallery = GallerySerializer()
    city = CitySerializer()
    user = UserSerializer()

    class Meta:
        model = Manager
        fields = ('id', 'user', 'full_name', 'phone_number', 'city', 'gallery')
