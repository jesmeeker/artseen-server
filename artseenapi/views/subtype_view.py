"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from artseenapi.models import SubType


@authentication_classes([])
@permission_classes([])
class SubTypeView(ViewSet):
    """Rare subtype view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single subtype
        Returns:
            Response -- JSON serialized subtype
        """
        try:

            # make connection with server to return single query set where the primary key matches the pk requested by the client and assigns the object instance found to the subtype variable
            subtype = SubType.objects.get(pk=pk)

        except SubType.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # passes the instance stored in subtype through serializer to become a JSON stringified object and assigns it to serializer variable
        serializer = SubTypeSerializer(subtype)

        # returns serializer data to the client as a response. Response body is JSON stringified object of requested data.
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        """Handle GET requests to get all cities
        Returns:
            Response -- JSON serialized list of cities
        """
        # Make connection with server to retrieve a query set of all cities items requested by client and assign the found instances to the cities variable
        cities = SubType.objects.order_by('label')
        # passes instances stored in cities variable to the serializer class to construct data into JSON stringified objects, which it then assigns to variable serializer
        serializer = SubTypeSerializer(cities, many=True)

        # Constructs response and returns data requested by the client in the response body as an array of JSON stringified objects
        return Response(serializer.data, status=status.HTTP_200_OK)

class SubTypeSerializer(serializers.ModelSerializer):
    """JSON serializer for game types"""
    # Converts meta data requested to JSON stringified object using Subtype as model
    class Meta:  # configuration for serializer
        model = SubType  # model to use
        fields = ('id', 'label')  # fields to include