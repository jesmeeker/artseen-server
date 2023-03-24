"""View module for handling requests about viewers"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from artseenapi.models import Viewer, City
from django.contrib.auth.models import User
from django.db.models import Q


class ViewerView(ViewSet):
    """Rare artist view"""

    def destroy(self, request, pk):
        viewer = Viewer.objects.get(pk=pk)
        viewer.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def list(self, request):
        """Handle GET requests for events

        Returns:
            Response -- JSON serialized events
        """
        viewers = Viewer.objects.all()

        if "user" in request.query_params:
            viewers = viewers.filter(user=request.auth.user)

        serializer = ViewerSerializer(viewers, many=True)
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

        viewer_to_update = Viewer.objects.get(pk=pk)
        viewer_to_update.phone_number = request.data['phone_number']
        viewer_to_update.city = city
        viewer_to_update.save()

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


class ViewerSerializer(serializers.ModelSerializer):
    """JSON serializer for artists
    """
    city = CitySerializer()
    user = UserSerializer()

    class Meta:
        model = Viewer
        fields = ('id', 'user', 'full_name', 'phone_number', 'city')
