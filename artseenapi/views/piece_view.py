"""View module for handling requests about pieces"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from artseenapi.models import Piece, PieceSubType, Artist, ArtType, SubType, Media, Surface


class PieceView(ViewSet):
    """Rare piece view"""

    def destroy(self, request, pk):
        piece = Piece.objects.get(pk=pk)
        piece.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, pk):
        """Handle GET requests for events

        Returns:
            Response -- JSON serialized events
        """
        artist = Artist.objects.get(user=request.auth.user)

        try:
            piece = Piece.objects.get(pk=pk)
            if piece.artist == artist:
                piece.creator = True

        except Piece.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = PieceSerializer(piece)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        """Handle GET requests to get all pieces

        Returns:
            Response -- JSON serialized list of pieces
        """
        pieces = []
        try:
            artist = Artist.objects.get(user=request.auth.user)
        except Artist.DoesNotExist:
            artist = None

        if "user" in request.query_params:
            pieces = Piece.objects.filter(artist_id=artist)
        
        if "artist" in request.query_params:
            artistId = request.query_params['artist']
            pieces = Piece.objects.filter(artist_id=artistId)

        else:
            pieces = Piece.objects.all()

        for piece in pieces:
            if artist is not None:
                if piece.artist == artist:
                    piece.creator = True

        serializer = PieceSerializer(pieces, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """Handle PIECE operations

        Returns
            Response -- JSON serialized game instance
        """
        try:
            artist = Artist.objects.get(user=request.auth.user)
        except Artist.DoesNotExist:
            return Response({'message': 'You sent an invalid token'}, status=status.HTTP_404_NOT_FOUND)

        try:
            arttype = ArtType.objects.get(pk=request.data['arttype'])
        except ArtType.DoesNotExist:
            return Response({'message': 'You sent an invalid arttype Id'}, status=status.HTTP_404_NOT_FOUND)

        try:
            media = Media.objects.get(pk=request.data['media'])
        except Media.DoesNotExist:
            return Response({'message': 'You sent an invalid media Id'}, status=status.HTTP_404_NOT_FOUND)

        piece = Piece.objects.create(
            artist=artist,
            title=request.data['title'],
            subtitle=request.data['subtitle'],
            arttype=arttype,
            media=media,
            length=request.data['length'],
            width=request.data['width'],
            height=request.data['height'],
            weight=request.data['weight'],
            image_url=request.data['image_url'],
            about=request.data['about'],
            available_purchase=request.data['available_purchase'],
            available_show=request.data['available_show'],
            will_ship=request.data['will_ship'],
            unique=request.data['unique'],
            quantity_available=request.data['qty_available'],
            price=request.data['price']
        )

        if request.data['surface'] is not None:
            try:
                surface = Surface.objects.get(pk=request.data['surface'])
                piece.surface = surface
                piece.save()
            except Surface.DoesNotExist:
                return Response({'message': 'You sent an invalid surface Id'}, status=status.HTTP_404_NOT_FOUND)
            
        else:
            pass

        subtypes_selected = request.data['subtypes']

        for subtype in subtypes_selected:
            piece_subtype = PieceSubType()
            piece_subtype.piece = piece
            piece_subtype.subtype = SubType.objects.get(pk=subtype)
            piece_subtype.save()

        serializer = PieceSerializer(piece)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PIECE operations

        Returns
            Response -- JSON serialized game instance
        """
        try:
            arttype = ArtType.objects.get(pk=request.data['arttype'])
        except ArtType.DoesNotExist:
            return Response({'message': 'You sent an invalid arttype Id'}, status=status.HTTP_404_NOT_FOUND)

        try:
            media = Media.objects.get(pk=request.data['media'])
        except Media.DoesNotExist:
            return Response({'message': 'You sent an invalid media Id'}, status=status.HTTP_404_NOT_FOUND)

        piece_to_update = Piece.objects.get(pk=pk)
        piece_to_update.title = request.data['title']
        piece_to_update.subtitle = request.data['subtitle']
        piece_to_update.arttype = arttype
        piece_to_update.media = media
        piece_to_update.length = request.data['length']
        piece_to_update.width = request.data['width']
        piece_to_update.height = request.data['height']
        piece_to_update.weight = request.data['weight']
        piece_to_update.image_url = request.data['image_url']
        piece_to_update.about = request.data['about']
        piece_to_update.available_purchase = request.data['available_purchase']
        piece_to_update.available_show = request.data['available_show']
        piece_to_update.will_ship = request.data['will_ship']
        piece_to_update.unique = request.data['unique']
        piece_to_update.quantity_available = request.data['quantity_available']
        piece_to_update.price = request.data['price']

        if request.data['surface'] is not None:
            try:
                surface = Surface.objects.get(pk=request.data['surface'])
                piece_to_update.surface = surface
            except Surface.DoesNotExist:
                return Response({'message': 'You sent an invalid surface Id'}, status=status.HTTP_404_NOT_FOUND)
            
        else:
            pass

        piece_to_update.save()

        subtypes_selected = request.data['subtypes']

        current_subtype_relationships = PieceSubType.objects.filter(
            piece__id=pk)
        current_subtype_relationships.delete()

        for subtype in subtypes_selected:
            piece_subtype = PieceSubType()
            piece_subtype.piece = piece_to_update
            piece_subtype.subtype = SubType.objects.get(pk=int(subtype))
            piece_subtype.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)


class PieceSubTypeSerializer(serializers.ModelSerializer):
    """JSON serializer for reactions
    """
    class Meta:
        model = SubType
        fields = ('id', 'label',)


class PieceArtistSerializer(serializers.ModelSerializer):
    """JSON serializer for reactions
    """
    class Meta:
        model = Artist
        fields = ('full_name',)


class PieceArtTypeSerializer(serializers.ModelSerializer):
    """JSON serializer for reactions
    """
    class Meta:
        model = ArtType
        fields = ('id', 'label',)


class PieceMediaSerializer(serializers.ModelSerializer):
    """JSON serializer for reactions
    """
    class Meta:
        model = Media
        fields = ('id', 'label',)


class PieceSurfaceSerializer(serializers.ModelSerializer):
    """JSON serializer for reactions
    """
    class Meta:
        model = Surface
        fields = ('id', 'label',)


class PieceSerializer(serializers.ModelSerializer):
    """JSON serializer for pieces
    """
    artist = PieceArtistSerializer()
    subtypes = PieceSubTypeSerializer(many=True)
    arttype = PieceArtTypeSerializer()
    media = PieceMediaSerializer()
    surface = PieceSurfaceSerializer()

    class Meta:
        model = Piece
        fields = ('id', 'artist', 'title', 'subtitle', 'arttype', 'subtypes', 'media', 'surface', 'length', 'width', 'height', 'weight', 'image_url', 'about', 'available_purchase', 'available_show', 'will_ship', 'unique', 'quantity_available', 'price', 'private', 'date_added', 'creator')
