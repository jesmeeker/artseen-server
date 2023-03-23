"""View module for handling requests about viewer profiles"""
import datetime
# from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from artseenapi.models import Order, Viewer, Piece
from artseenapi.models import OrderPiece
from .piece_view import PieceSerializer
from .order_view import OrderSerializer
from django.contrib.auth.models import User


class Profile(ViewSet):
    """Request handlers for user profile info in the Artseen Platform"""
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def list(self, request):
        """_summary_

        Args:
            request (_type_): _description_
        """
        profiles = User.objects.all()
        serializer = ProfileSerializer(
            profiles, many=False, context={'request': request})

        return Response(serializer.data)

    @action(methods=['get', 'post', 'delete'], detail=False)
    def cart(self, request, pk=None):
        """Shopping cart manipulation"""

        current_user = Viewer.objects.get(user=request.auth.user)

        if request.method == "DELETE":
            if pk is not None:
                line_item = OrderPiece.objects.get(piece_id=pk)
                line_item.delete()

            else:
                try:
                    open_order = Order.objects.get(
                        viewer=current_user, payment_type=None)
                    line_items = OrderPiece.objects.filter(order=open_order)
                    line_items.delete()
                    open_order.delete()
                except Order.DoesNotExist as ex:
                    return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        if request.method == "GET":
            try:
                open_order = Order.objects.get(
                    viewer=current_user, payment_type=None)

                cart = {}
                cart["order"] = OrderSerializer(open_order, many=False, context={
                                                'request': request}).data

            except Order.DoesNotExist as ex:
                return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

            return Response(cart["order"])

        if request.method == "POST":
            try:
                open_order = Order.objects.get(
                    viewer=current_user, payment_type__isnull=True)
                print(open_order)
            except Order.DoesNotExist:
                open_order = Order()
                open_order.created_date = datetime.datetime.now()
                open_order.viewer = current_user
                open_order.save()

            line_item = OrderPiece()
            line_item.piece = Piece.objects.get(
                pk=request.data["piece_id"])
            line_item.order = open_order
            line_item.save()

            line_item_json = LineItemSerializer(
                line_item, many=False, context={'request': request})

            return Response(line_item_json.data)

        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class LineItemSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for pieces

    Arguments:
        serializers
    """
    piece = PieceSerializer(many=False)

    class Meta:
        model = OrderPiece
        fields = ('id', 'piece')
        depth = 1


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for viewer profile

    Arguments:
        serializers
    """
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        depth = 1


class ViewerSerializer(serializers.ModelSerializer):
    """JSON serializer for recommendation viewers"""
    user = UserSerializer()

    class Meta:
        model = Viewer
        fields = ('id', 'user',)


class ProfilePieceSerializer(serializers.ModelSerializer):
    """JSON serializer for pieces"""
    class Meta:
        model = Piece
        fields = ('id', 'name',)


class ProfileSerializer(serializers.ModelSerializer):
    """JSON serializer for viewer profile

    Arguments:
        serializers
    """
    user = UserSerializer(many=False)

    class Meta:
        model = Viewer
        fields = ('id', 'url', 'user', 'phone_number',
                  'address', 'payment_types', 'recommends', 'recommendations')
        depth = 1