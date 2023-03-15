"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from artseenapi.models import SubType, ArtSubRelationship, ArtType

class SubTypeView(ViewSet):
    """Rare subtype view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single subtype
        Returns:
            Response -- JSON serialized subtype
        """
        try:
            subtype = SubType.objects.get(pk=pk)

        except SubType.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = SubTypeSerializer(subtype)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        """Handle GET requests to get all cities
        Returns:
            Response -- JSON serialized list of cities
        """
        subtypes = SubType.objects.order_by('label')
        
        if "arttypeId" in request.query_params:
            arttypeId = int(request.query_params['arttypeId'])
            subtypes = subtypes.filter(subtypes_of_arttype__id=arttypeId)

        serializer = SubTypeSerializer(subtypes, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class SubTypeSerializer(serializers.ModelSerializer):
    """JSON serializer for game types"""
    class Meta:  
        model = SubType  
        fields = ('id', 'label') 