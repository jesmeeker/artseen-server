"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from artseenapi.models import Gallery, City


@authentication_classes([])
@permission_classes([])
class GalleryView(ViewSet):
    """Rare gallery view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single gallery
        Returns:
            Response -- JSON serialized gallery
        """
        try:
            gallery = Gallery.objects.get(pk=pk)

        except Gallery.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = GallerySerializer(gallery)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        """Handle GET requests to get all cities
        Returns:
            Response -- JSON serialized list of cities
        """
        galleries = Gallery.objects.all()

        if "city" in request.query_params:
            city_id = int(request.query_params['city'])
            city = City.objects.get(pk=city_id)
            galleries = galleries.filter(city=city)

        serializer = GallerySerializer(galleries, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class CitySerializer(serializers.ModelSerializer):
    """JSON serializer for artists
    """

    class Meta:
        model = City
        fields = ('id', 'label')

class GallerySerializer(serializers.ModelSerializer):
    """JSON serializer for game types"""
    
    class Meta:  
        model = Gallery  
        fields = ('id', 'name', 'address', 'phone',
                  'square_feet', 'rooms', 'city') 
