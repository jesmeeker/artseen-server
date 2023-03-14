"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.decorators import authentication_classes, api_view, permission_classes
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from artseenapi.models import City

@authentication_classes([])
@permission_classes([])
class CityView(ViewSet):
    """Rare citys view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single city
        Returns:
            Response -- JSON serialized city
        """
        try:

            city = City.objects.get(pk=pk) #make connection with server to return single query set where the primary key matches the pk requested by the client and assigns the object instance found to the city variable
        
        except City.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CitySerializer(city) #passes the instance stored in city through serializer to become a JSON stringified object and assigns it to serializer variable

        return Response(serializer.data, status=status.HTTP_200_OK) # returns serializer data to the client as a response. Response body is JSON stringified object of requested data.

    def list(self, request):
        """Handle GET requests to get all cities
        Returns:
            Response -- JSON serialized list of cities
        """
        # Make connection with server to retrieve a query set of all cities items requested by client and assign the found instances to the cityies variable
        # citys = City.objects.all()
        cities = City.objects.order_by('label')
        #passes instances stored in citys variable to the serializer class to construct data into JSON stringified objects, which it then assigns to variable serializer
        serializer = CitySerializer(cities, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK) #Constructs response and returns data requested by the client in the response body as an array of JSON stringified objects
        
    def create(self, request):
            """Handle POST operations
            Returns
                Response -- JSON serialized city instance
            """

            city = City.objects.create(
                label=request.data["label"]
            )
            serializer = CitySerializer(city)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a city
        Returns:
            Response -- Empty body with 204 status code
        """

        city = City.objects.get(pk=pk)
        city.label = request.data["label"]
        city.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        city = City.objects.get(pk=pk)
        city.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class CitySerializer(serializers.ModelSerializer):
    """JSON serializer for game types"""
    # Converts meta data requested to JSON stringified object using City as model
    class Meta: # configuration for serializer
        model = City # model to use
        fields = ('id', 'label') # fields to include