"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from artseenapi.models import Surface, Artist


class SurfaceView(ViewSet):
    """Rare surface view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single surface
        Returns:
            Response -- JSON serialized surface
        """
        try:
            surface = Surface.objects.get(pk=pk)

        except Surface.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = SurfaceSerializer(surface)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        """Handle GET requests to get all cities
        Returns:
            Response -- JSON serialized list of cities
        """
        surfaces = Surface.objects.order_by('label')
        serializer = SurfaceSerializer(surfaces, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ArtistSerializer(serializers.ModelSerializer):
    """JSON serializer for reactions
    """
    class Meta:
        model = Artist
        fields = ('full_name',)


class SurfaceSerializer(serializers.ModelSerializer):
    """JSON serializer for game types"""

    artist = ArtistSerializer()

    class Meta:
        model = Surface
        fields = ('id', 'label', 'artist')
